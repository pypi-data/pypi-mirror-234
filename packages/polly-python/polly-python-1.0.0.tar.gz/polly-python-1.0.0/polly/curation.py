import json
from collections import namedtuple
import os
import shutil
from typing import Dict, Optional, List
import warnings
import pandas as pd
from functools import lru_cache
from polly.errors import (
    InvalidSchemaJsonException,
    InvalidSyntaxForRequestException,
    EmptyPayloadException,
    RequestException,
    UnauthorizedException,
    extract_json_api_error,
    paramException,
)
from polly.auth import Polly
from polly.cohort import Cohort
from polly import helpers, constants as const, application_error_info as app_err_info
from polly.help import example
import polly.http_response_codes as http_codes
from polly.constants import SUPPORTED_ENTITY_TYPES, CURATION_COHORT_CACHE
from polly.helpers import get_cohort_constants
from polly.tracking import Track


class Curation:
    """
    The Curation class contains wrapper functions around the models used for
    semantic annotations of string/text.
    Args:
        token (str): token copy from polly.

    Usage:
            from polly.curation import Curation

            curationObj = Curation(token)
    """

    Tag = namedtuple("Tag", ["name", "ontology_id", "entity_type"])
    example = classmethod(example)

    def __init__(
        self,
        token=None,
        env="",
        default_env="polly",
    ) -> None:
        # check if COMPUTE_ENV_VARIABLE present or not
        # if COMPUTE_ENV_VARIABLE, give priority
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self.discover_url = f"https://api.discover.{self.session.env}.elucidata.io"
        self.elastic_url = (
            f"https://api.datalake.discover.{self.session.env}.elucidata.io/elastic/v2"
        )
        self.inference_url = f"https://api.discover.{self.session.env}.elucidata.io/curations/inferences/"
        self.cohort = Cohort()
        self.cohort_constants = get_cohort_constants()

    def _handle_errors(self, response):
        detail = response.get("errors")[0].get("detail", [])
        title = response.get("errors")[0].get("title", [])
        return title, detail

    def _fetch_metadata_from_cohort(self, repo_name: str, dataset_ids: List[str]):
        """
        Utility function for fetching metadata using cohorts.

        Arguments:
            repo_name (str) : name of the repository for fetching datasets.
            dataset_ids (List[str]): dataset ids to be used for inference

        Returns:
            Returns sample metadata, dataset and sample ids.
        """
        sample_metadata = {}
        dataset_to_sample_id = {"dataset_id": [], "sample_id": []}

        if not (os.path.isdir(CURATION_COHORT_CACHE)):
            os.mkdir(CURATION_COHORT_CACHE)
        else:
            shutil.rmtree(CURATION_COHORT_CACHE)
            os.mkdir(CURATION_COHORT_CACHE)

        self.cohort.create_cohort(
            CURATION_COHORT_CACHE, "sample_metadata_query", "desc"
        )

        # Fetch metadata using cohorts
        for dataset_id in dataset_ids:
            datasets_sample_metadata = []

            if not (
                repo_name in self.cohort_constants
                and self.cohort_constants[repo_name]["file_structure"] != "multiple"
            ):
                # multiple mapped repo such as GEO
                self.cohort.add_to_cohort(repo_name, dataset_id=dataset_id)
            else:
                # for single mapped repos such as TCGA
                self.cohort.add_to_cohort(repo_name, dataset_id=[dataset_id])

            col_metadata = self.cohort.merge_data("sample")
            all_sample_ids = col_metadata.index.tolist()

            col_metadata.loc[:, "dataset_id"] = dataset_id
            dataset_to_sample_id["dataset_id"] += [dataset_id] * len(all_sample_ids)

            col_metadata.loc[:, "sample_id"] = all_sample_ids
            dataset_to_sample_id["sample_id"] += all_sample_ids

            datasets_sample_metadata += list(col_metadata.T.to_dict().values())

            if not (
                repo_name in self.cohort_constants
                and self.cohort_constants[repo_name]["file_structure"] != "multiple"
            ):
                self.cohort.remove_from_cohort(dataset_id)
            else:
                self.cohort.remove_from_cohort([dataset_id])

            sample_metadata[dataset_id] = datasets_sample_metadata

        dataset_to_sample_id = pd.DataFrame.from_dict(dataset_to_sample_id)

        return sample_metadata, dataset_to_sample_id

    def _clinical_model_param_checks(
        self,
        repo_name: str,
        dataset_ids: List[str],
        sample_ids: Optional[List[str]] = None,
    ):
        """
        Checking the parameter passed to the clinical label assigning model.

        Arguments:
            repo_name (str): repo name
            dataset_ids (list[str]): list of dataset ids

        Keyword Arguments:
            sample_ids (list[str], optional): Optional Parameter. List of sample ids.
            Default is 'None'.

        Raises:
            paramException
        """
        if dataset_ids is None or type(dataset_ids) is not list:
            raise paramException(
                title="Param Exception",
                detail="Dataset IDs should be given as a valid list of strings",
            )

        if sample_ids is not None and type(sample_ids) is not list:
            raise paramException(
                title="Param Exception",
                detail="Sample IDs should be given as a valid list of strings",
            )

        if repo_name != "geo" and not any(
            ["GSE" in dataset_id for dataset_id in dataset_ids]
        ):
            warnings.warn(
                "The model is tested with GEO metadata and the labels may be wrong for other repos"
            )

    def _post_process_clinical_tags(
        self,
        clinical_tags: pd.DataFrame,
        is_sample_tag: bool,
        sample_ids: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        process the response of the model (dataframe with clinical tags and samples)
        and return relevant feilds.
        incase no sample_ids are provided by the user, we return the dataset_ids and the clinical tags
        incase sample_ids are also provided, then we return the dataset_ids, the sample_ids and the clincal tags.

        Arguments:
            clinical_tags (pd.DataFrame): dataframe of the sample_ids and assigned clinical tags
            is_sample_tag (bool): if samples passed

        Keyword Arguments:
            sample_ids (list[str]): list of sample ids (default: {None})

        Returns:
            a dataframe with the the dataset_ids, sample_ids and the assigned clinical tags
        """
        if is_sample_tag:
            # if the user has provided list of samples, then we filter in just those sample ids
            # for the dataset ids.
            # taking only those clinical tags and samples where the sample_ids are in the sample_id list
            # provided by the user.
            clinical_tags = clinical_tags[
                clinical_tags["sample_id"].isin(sample_ids)
            ].reset_index(drop=True)

            # in case the sample_ids provided by the user are not present in the dataset_ids provided.
            if clinical_tags.empty or clinical_tags.shape[0] < len(sample_ids):
                warnings.warn(
                    "The output is empty or has missing sample ids because they are not present in given datasets."
                )

            # return sample level tags here
            return clinical_tags
        # if no sample_ids were passed by the user, then
        # returning dataset level tags by removing sample id and removing duplicate columns
        return (
            clinical_tags.drop(columns=["sample_id"])
            .drop_duplicates()
            .reset_index(drop=True)
        )

    def _handle_perform_inference_api_error(self, response):
        if response.status_code == http_codes.UNAUTHORIZED:
            raise UnauthorizedException("User is unauthorized to access this")
        elif response.status_code == http_codes.BAD_REQUEST:
            title, details = extract_json_api_error(response)
            if title == app_err_info.EMPTY_PAYLOAD_CODE:
                raise EmptyPayloadException()
            elif app_err_info.INVALID_MODEL_NAME_TITLE in title:
                raise InvalidSyntaxForRequestException()
        elif response.status_code == http_codes.INTERNAL_SERVER_ERROR:
            raise InvalidSchemaJsonException()
        elif response.status_code == http_codes.GATEWAY_TIMEOUT:
            error_detail = response.json().get("message", "Request timed out")
            raise Exception(error_detail)
        else:
            title, details = extract_json_api_error(response)
            raise Exception("Exception Occurred :" + str(details))

    def _perform_inference(
        self,
        model_name: str,
        input_data: dict,
    ) -> dict:
        """
        This is a wrapper around model inference APIs
        It serializes input_data, calls the API for the given model_name
        and returns deserialized output.

        Args:
            model_name (str): one of 'normalizer', 'biobert' and 'control-perturbation'
            input_data (dict): model input

        Returns:
            dict
        """
        url = self.inference_url + model_name

        payload = {}
        payload = json.dumps({"data": {"attributes": input_data, "type": "curation"}})
        response = self.session.post(url, data=payload)
        try:
            if response.status_code != 201:
                self._handle_perform_inference_api_error(response)
        except Exception as err:
            raise err
        try:
            response = response.json()
        except json.JSONDecodeError as e:
            raise e
        if "data" in response:
            return response.get("data")
        return response

    @Track.track_decorator
    @lru_cache(maxsize=None)
    def standardise_entity(
        self,
        mention: str,
        entity_type: str,
        context: Optional[str] = None,
        threshold: Optional[float] = None,
    ) -> dict:
        """
        Map a given mention (keyword) to an ontology term.
        Given a text and entity type, users can get the Polly compatible ontology for the text such as the MESH ontology.

        Args:
            mention (str): mention of an entity e.g. "Cadiac arrythmia"
            entity_type (str): Should be one of\
            ['disease', 'drug', 'tissue', 'cell_type', 'cell_line', 'species', 'gene']
            context (str): The text where the mention occurs.\
            This is used to resolve abbreviations.
            Threshold: (float, optional) = Optional Parameter. \
            All entities with a score < threshold are filtered out from the output. \
            Its best not to specify a threshold and just use the default value instead.

        Returns:
            dict : Dictionary containing keys and values of the entity type,
            ontology (such as NCBI, MeSH), ontology ID (such as the MeSH ID), the score (confidence score), and synonyms if any
        Raises:
            requestException : Invalid Request
        """
        data = {
            "mention": {
                "keyword": mention,
                "entity_type": entity_type,
                "threshold": threshold,
            }
        }

        if context:
            data["context"] = context
        output = self._perform_inference("normalizer", data)
        if output.get("errors", []):
            title, detail = self._handle_errors(output)
            raise RequestException(title, detail)

        if "term" not in output:
            return {
                "ontology": "CUI-less",
                "ontology_id": None,
                "name": None,
                "entity_type": entity_type,
            }

        return output.get("term", [])

    @Track.track_decorator
    def recognise_entity(
        self,
        text: str,
        threshold: Optional[float] = None,
        normalize_output: bool = False,
    ):
        """
        Run an NER model on the given text. The returned value is a list of entities along with span info.
        Users can simply recognise entities in a given text without any ontology standardisation
         (unlike the annotate_with_ontology function which normalises as well).

        Args:
            text (str): input text
            threshold (float, optional): Optional Parameter. \
            All entities with a score < threshold are filtered out from the output. \
            Its best not to specify a threshold and just use the default value instead.\
            normalize_output (bool): whether to normalize the keywords

        Returns:
            entities (List[dict]): List of spans containing the keyword, start/end index of the keyword and the entity type
        Raises:
            requestException : Invalid Request
        """
        # TODO: If text is too long, break it up into chunks small enough for biobert

        payload = {"text": text}
        if threshold:
            payload["threshold"] = threshold
        response = self._perform_inference("biobert", payload)
        if response.get("errors", []):
            title, detail = self._handle_errors(response)
            raise RequestException(title, detail)
        try:
            entities = response.get("entities", [])
        except KeyError as e:
            raise e

        # TODO: fetch this list from the server maybe?

        if normalize_output:
            for entity in entities:
                # don't call `normalize` for unsupported entity types
                if entity.get("entity_type") not in SUPPORTED_ENTITY_TYPES:
                    entity["name"] = None
                    continue
                norm = self.standardise_entity(
                    entity["keyword"], entity["entity_type"], text
                )
                if norm.get("ontology", []) == "CUI-less":
                    entity["name"] = None
                else:
                    entity["ontology_id"] = norm["ontology"] + ":" + norm["ontology_id"]
                    entity["name"] = norm["name"]
        return entities

    @Track.track_decorator
    def annotate_with_ontology(
        self,
        text: str,
    ) -> List[Tag]:
        """
        Tag a given piece of text. A "tag" is just an ontology term. Annotates with Polly supported ontologies.
        This function calls recognise_entity followed by normalize.
        Given a text, users can identify and tag entities in a text.
        Each entity/tag recognised in the text contains the name(word in the text identified), entity_type and the ontology_id.

        Args:
            text (str): Input text
        Returns:
            set of unique tags
        """

        entities = self.recognise_entity(text, normalize_output=True)
        res = {
            self.Tag(
                e.get("name", []), e.get("ontology_id", []), e.get("entity_type", [])
            )
            for e in entities
            if e.get("name")
        }
        return list(res)

    @Track.track_decorator
    def find_abbreviations(self, text: str) -> Dict[str, str]:
        """
        To run abbreviation detection separately.
        Internally calls a normaliser.

        Args:
            text (str): The string to detect abbreviations in.

        Returns:
        Dictionary with abbreviation as key and full form as value

        Raises:
            requestException : Invalid Request
        """
        data = {
            "mention": {"keyword": "dummykeyword", "entity_type": "gene"},
            "context": text,
        }

        response = self._perform_inference("normalizer", data)
        if "errors" in response:
            title, detail = self._handle_errors(response)
            raise RequestException(title, detail)
        try:
            output = response.get("abbreviations", [])
        except KeyError as e:
            raise e

        return output

    def assign_control_pert_labels(
        self, sample_metadata, columns_to_exclude=None
    ) -> pd.DataFrame:
        """Returns the sample metadata dataframe with 2 additional columns.
            is_control - whether the sample is a control sample
            control_prob - the probability that the sample is control
        Args:
            sample_metadata (DataFrame): Metadata table
            columns_to_exclude (Set[str]): Any columns which don't play any role in determining the label, e.g. sample id
        Returns:
            DataFrame : Input data frame with 2 additional columns
        Raises:
            requestException : Invalid Request

        """
        sample_metadata = sample_metadata.copy()

        if columns_to_exclude is None:
            columns_to_exclude = []

        cols = sample_metadata.columns.difference(columns_to_exclude)

        samples = sample_metadata[cols].to_dict("records")
        request_body = {"samples": samples}
        response = self._perform_inference("control-pertubation", request_body)
        response = {
            k: v for k, v in response.items() if k != "version" and k != "testing"
        }
        if "errors" in response:
            title, detail = self._handle_errors(response)
            raise RequestException(title, detail)
        try:
            output = pd.DataFrame(response)
        except KeyError as e:
            raise e
        sample_metadata["is_control"] = output["is_control"].values
        sample_metadata["control_prob"] = output["control_prob"].values
        return sample_metadata

    @Track.track_decorator
    def assign_clinical_labels(
        self,
        repo_name: str,
        dataset_ids: List[str],
        sample_ids: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Returns a list of clinical or non clinical labels for the given datasets or samples.

        Arguments:
            repo_name (str): name of the repository for fetching datasets.
            dataset_ids (List[str]): dataset ids to be used for inference

        Keyword Arguments:
            sample_ids (List[str], optional): Optional Parameter. Sample ids if that is needed.

        Raises:
            RequestException: API response exception
            ParamException: Invalid parameters
            err

        Returns:
            dataframe which is a list of clinical tags for given ids
        """
        warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"

        try:
            self._clinical_model_param_checks(repo_name, dataset_ids, sample_ids)
            # evaluating the inference level based on if the user has provided sample_ids
            is_sample_tag = sample_ids is not None
            inference_level = "sample_id" if (is_sample_tag) else "dataset_id"

            sample_metadata, dataset_to_sample_id = self._fetch_metadata_from_cohort(
                repo_name=repo_name, dataset_ids=dataset_ids
            )

            clinical_model_predictions = []

            for dataset_id in sample_metadata:
                # Get output from model endpoint and structure output
                payload = {
                    "sample_metadata": sample_metadata[dataset_id],
                    "sample_id_column": "sample_id",
                    "dataset_id_column": "dataset_id",
                    "is_sample_tag": is_sample_tag,
                }

                output = self._perform_inference("clinical-classifier", payload)
                if "errors" in output:
                    title, detail = self._handle_errors(output)
                    raise RequestException(title, detail)

                output = output["clinical_predictions"]

                clinical_model_predictions += output

            # creating dataframe with inference_level and clinical_tags with values from the clinical_model_predictions
            clinical_tags = pd.DataFrame(
                {
                    inference_level: [
                        tag["tag_id"] for tag in clinical_model_predictions
                    ],
                    "clinical_tag": [
                        tag["clinical_tag"] for tag in clinical_model_predictions
                    ],
                }
            )

            clinical_tags = pd.merge(
                dataset_to_sample_id, clinical_tags, on=inference_level
            )

            clinical_tags = self._post_process_clinical_tags(
                clinical_tags, is_sample_tag, sample_ids
            )
        except Exception as err:
            raise err

        return clinical_tags
