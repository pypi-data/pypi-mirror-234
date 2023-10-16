import os
import ssl
import json
import base64
from polly import helpers
from tqdm import tqdm
import urllib.request
import logging
from polly.omixatlas import OmixAtlas
from polly.errors import (
    InvalidCohortNameException,
    paramException,
    InvalidParameterException,
    InvalidPathException,
    InvalidDatasetException,
    TechnicalFaultException,
    InvalidDatatypeException,
    IncompatibleDataSource,
    error_handler,
)
from polly.constants import COHORT_VERSION, dot
from joblib import Parallel, delayed
import datetime
from cmapPy.pandasGEXpress.parse import parse
from polly.core_cohort import CohortFileStandard


class CohortRepoClass:
    """
    The Class responsible for Encapsulating Cohort Bridge Functionalities.
    These are the functionalities that extend other useful features from OmixAtlas.
    """

    def __init__(self, session) -> None:
        self.session = session
        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self._cohort_details = None

    def add_to_cohort_single(
        self,
        cohort_path: str,
        repo_name: str,
        entity_id: list,
        entity_type: str,
    ):
        """
        Function to add dataset_id to cohort for single file structure repositories
        """
        print("Initializing process...")
        obj = CohortFileStandard()
        if not (entity_id and isinstance(entity_id, list)):
            raise InvalidParameterException(
                "entity_id(list) for single file structure repositories"
            )
        datatype_dict = {}
        with helpers.tqdm_joblib(tqdm(desc="Verifying Data", total=len(entity_id))):
            datatype_list = Parallel(n_jobs=20, require="sharedmem")(
                delayed(self._return_datatype_dict)(repo_name, i) for i in entity_id
            )
        for id in range(0, len(entity_id)):
            datatype_dict[entity_id[id]] = datatype_list[id]
        dataset_id = self._validate_dataset(entity_id, datatype_dict)
        with helpers.tqdm_joblib(
            tqdm(desc="Adding data to cohort", total=len(dataset_id))
        ):
            status_gct = Parallel(n_jobs=20, require="sharedmem")(
                delayed(self._gctfile)(repo_name, i, cohort_path) for i in dataset_id
            )
        with helpers.tqdm_joblib(
            tqdm(desc="Adding metadata to cohort", total=len(dataset_id))
        ):
            status_jpco = Parallel(n_jobs=20, require="sharedmem")(
                delayed(self._add_metadata)(repo_name, i, cohort_path)
                for i in dataset_id
            )
        dataset_id, deleted_id = obj._rollback_files(
            status_gct, status_jpco, repo_name, cohort_path, dataset_id
        )
        file_meta = helpers.make_path(cohort_path, "cohort.meta")
        tuple_list = self._get_datatype(repo_name, dataset_id, cohort_path)
        self._cohort_details = obj._update_metadata_single(
            repo_name, entity_type, dataset_id, deleted_id, file_meta, tuple_list
        )

    def _add_metadata(self, repo_key: str, dataset_id: str, local_path: str) -> None:
        """
        Function to add dataset level metadata to a cohort.
        Returns 0 on successful download, dataset_id on failure.
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_id/repo_name")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        try:
            metadata = self._get_metadata(repo_key, dataset_id)
            file_name = f"{repo_key}_{dataset_id}.jpco"
            file_name = helpers.make_path(local_path, file_name)
            with open(file_name, "w") as outfile:
                json.dump(metadata, outfile)
            return 0
        except Exception:
            return dataset_id

    def _gctfile(self, repo_info: str, dataset_id: str, file_path: str) -> None:
        """
        Function to add gct file to a cohort
        Returns 0 on successful download, dtaset_id on failure.
        """
        try:
            if not (repo_info and isinstance(repo_info, str)):
                raise InvalidParameterException("repo_name/repo_id")
            if not (dataset_id and isinstance(dataset_id, str)):
                raise InvalidParameterException("dataset_id")
            ssl._create_default_https_context = ssl._create_unverified_context
            obj = OmixAtlas()
            download_dict = obj.download_data(repo_info, dataset_id, internal_call=True)
            url = (
                download_dict.get("data", {}).get("attributes", {}).get("download_url")
            )
            file_name = f"{repo_info}_{dataset_id}.gct"
            dest_path = helpers.make_path(file_path, file_name)
            urllib.request.urlretrieve(url, dest_path)
            return 0
        except Exception:
            return dataset_id

    def create_cohort(self, local_path: str, cohort_name: str, description: str) -> str:
        """
        This function is used to create a cohort
        Args:
            | local_path(str): local path to instantiate the cohort
            | cohort_name(str): identifier name for the cohort
            | description(str): description about the cohort
            | repo_key(str): Optional argument: repo_key(repo_name/repo_id) for the omixatlas to be added
            | entity_id(list): Optional argument: list of sample_id or dataset_id to be added to the cohort
        Returns:
            | A confirmation message on creation of cohort
        """
        if not (local_path and isinstance(local_path, str)):
            raise InvalidParameterException("local_path")
        if not (cohort_name and isinstance(cohort_name, str)):
            raise InvalidParameterException("cohort_name")
        if not (description and isinstance(description, str)):
            raise InvalidParameterException("description")
        if not os.path.exists(local_path):
            raise InvalidPathException
        if dot in cohort_name:
            raise InvalidCohortNameException(cohort_name)
        file_path = os.path.join(local_path, f"{cohort_name}.pco")
        user_id = self._get_user_id()
        os.makedirs(file_path)
        metadata = {
            "number_of_datasets": 0,
            "entity_id": {},
            "source_omixatlas": {},
            "description": description,
            "user_id": user_id,
            "date_created": str(datetime.datetime.now()),
            "version": COHORT_VERSION,
        }
        file_name = os.path.join(file_path, "cohort.meta")
        input = json.dumps(metadata)
        with open(file_name, "wb") as outfile:
            encoded_data = base64.b64encode(input.encode("utf-8"))
            outfile.write(encoded_data)
        logging.basicConfig(level=logging.INFO)
        logging.info("Cohort Created !")
        self._cohort_details = metadata
        return str(file_path)

    def _get_user_id(self):
        """
        Function to get user id
        """
        me_url = f"{self.base_url}/users/me"
        details = self.session.get(me_url)
        error_handler(details)
        user_id = details.json().get("data", {}).get("attributes", {}).get("user_id")
        return user_id

    def _get_datatype(self, repo_name: str, dataset_id: list, cohort_path: str) -> list:
        datatype_list = []
        for i in dataset_id:
            file_name = f"{repo_name}_{i}.jpco"
            file_name = helpers.make_path(cohort_path, file_name)
            if os.path.exists(file_name):
                with open(file_name, "r") as infile:
                    temp_df = json.load(infile)
                    data_type = temp_df.get("_source", {}).get("data_type")
                    dataset_tuple = [repo_name, data_type]
                    datatype_list.append(dataset_tuple)
        return datatype_list

    def _return_datatype_dict(self, repo_name: str, dataset_id: str):
        metadata = self._get_metadata(repo_name, dataset_id)
        datatype = metadata.get("_source", {}).get("data_type")
        return datatype

    def _get_metadata(self, repo_key: str, dataset_id: str) -> dict:
        """
        Function to return metadata for a dataset
        """
        obj = OmixAtlas()
        response_omixatlas = obj.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data")
        index_name = data.get("indexes", {}).get("files")
        if index_name is None:
            raise paramException(
                title="Param Error", detail="Repo entered is not an omixatlas."
            )
        elastic_url = f"{obj.elastic_url}/{index_name}/_search"
        query = helpers.elastic_query(index_name, dataset_id)
        metadata = helpers.get_metadata(obj, elastic_url, query)
        return metadata

    def _validate_dataset(self, dataset_id: list, datatype_dict: dict) -> list:
        """
        Function to validate repo and datasets given as argument for adding to cohort
        """
        dataset_list = list(self._cohort_details["entity_id"].keys())
        valid_dataset_id = []
        dataset_id = list(set(dataset_id))
        for dataset in dataset_id:
            if dataset in dataset_list:
                logging.basicConfig(level=logging.INFO)
                logging.info(
                    f"The entity_id - {dataset} is already existing in the cohort."
                )
                continue
            datatype = datatype_dict[dataset]
            result = helpers.validate_datatype(datatype)
            if result:
                logging.basicConfig(level=logging.INFO)
                logging.info(
                    f"The entity_id - {dataset} has datatype - 'Single cell' that is not incorporated.\
                     Please contact Polly Support."
                )
                continue
            valid_dataset_id.append(dataset)
        if len(valid_dataset_id) == 0:
            raise InvalidDatasetException
        return valid_dataset_id

    def add_to_cohort_multiple(
        self,
        cohort_path: str,
        repo_name: str,
        dataset_id: str,
        sample_id: list,
        entity_type: str,
    ):
        """
        Function to add samples to cohort for multiple file structure repositories
        """
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException(
                "dataset_id(str) required for multiple file structure repository."
            )
        print("Initializing process...")
        metadata = self._get_metadata(repo_name, dataset_id)
        datatype = metadata.get("_source", {}).get("data_type")
        result = helpers.validate_datatype(datatype)
        if result:
            raise InvalidDatatypeException()
        dataset_list = list(self._cohort_details["entity_id"].keys())
        gct_file_name = f"{repo_name}_{dataset_id}.gct"
        jpco_file_name = f"{repo_name}_{dataset_id}.jpco"
        gct_path = helpers.make_path(cohort_path, gct_file_name)
        jpco_path = helpers.make_path(cohort_path, jpco_file_name)
        status = self._download_files_multiple(
            repo_name, dataset_id, dataset_list, cohort_path, gct_path, jpco_path
        )
        if status is None:
            raise TechnicalFaultException()
        download_flag = status
        data = parse(gct_path)
        cids = list(data.col_metadata_df.index)
        if sample_id is None or len(sample_id) == 0:
            sample_id = cids
        status_sample_id = []
        for i in sample_id:
            if i not in cids:
                status_sample_id.append(0)
            else:
                status_sample_id.append(1)
        file_meta = helpers.make_path(cohort_path, "cohort.meta")
        if 1 not in status_sample_id:
            print("Invalid samples, please try again.")
            if download_flag:
                os.remove(gct_path)
                os.remove(jpco_path)
        else:
            obj = CohortFileStandard()
            dataset_tuple = [
                repo_name,
                datatype,
            ]
            self._cohort_details = obj._update_metadata_multiple(
                repo_name,
                entity_type,
                dataset_id,
                sample_id,
                download_flag,
                file_meta,
                status_sample_id,
                dataset_tuple,
            )

    def _download_files_multiple(
        self, repo_name, dataset_id, dataset_list, local_path, gct_path, jpco_path
    ):
        download_flag = 0
        if dataset_id not in dataset_list:
            print("Adding data to cohort...")
            status_gct = self._gctfile(repo_name, dataset_id, local_path)
            print("Adding metadata to cohort...")
            status_jpco = self._add_metadata(repo_name, dataset_id, local_path)
            if not (status_gct == 0 and status_jpco == 0):
                if os.path.exists(gct_path):
                    os.remove(gct_path)
                if os.path.exists(jpco_path):
                    os.remove(jpco_path)
                return None
            download_flag = 1
        return download_flag

    def _return_omixatlas_name(self, repo_key: str):
        obj = OmixAtlas()
        response_omixatlas = obj.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data")
        repo_name = data.get("repo_name")
        return repo_name

    def _get_entity_type(self, repo_name, dataset_id, cohort_constants):
        """
        Function to return the entity type for the hybrid omixatlases.
        Input: repo_name(str), dataset_id(str or list), cohort_constants(json)
        Returns: Entity_type('dataset' for single mapped repositories,\
            'sample' for multiple mapped repositories.)
        """
        if isinstance(dataset_id, list):
            with helpers.tqdm_joblib(
                tqdm(desc="Validating datasets", total=len(dataset_id))
            ):
                source_list = Parallel(n_jobs=20, require="sharedmem")(
                    delayed(self._return_data_source)(repo_name, dataset)
                    for dataset in dataset_id
                )
            # removing duplicate results
            unique_source = list(set(source_list))
            if len(unique_source) == 1 and unique_source[0] is None:
                # raising exception in case of wrong input
                raise TechnicalFaultException()
            # if more than one data sources, then check for compatibility
            if len(unique_source) > 1:
                entity_list = []
                for source in unique_source:
                    if source is None:
                        continue
                    entity_type = helpers.return_entity_type(
                        source.lower(), cohort_constants
                    )
                    if entity_type is not None:
                        entity_list.append(entity_type)
                entities = list(set(entity_list))
                if len(entities) > 1:
                    raise IncompatibleDataSource(unique_source)
                return entities[0]
            else:
                entity_type = helpers.return_entity_type(
                    unique_source[0].lower(), cohort_constants
                )
                return entity_type
        elif isinstance(dataset_id, str):
            data_source = self._return_data_source(repo_name, dataset_id)
            if data_source is None:
                raise TechnicalFaultException()
            entity_type = helpers.return_entity_type(
                data_source.lower(), cohort_constants
            )
            return entity_type
        else:
            # Invalid value for argument dataset_id
            raise InvalidParameterException("entity_id")

    def _return_data_source(self, repo_name, dataset_id):
        """
        Function to return the data source for a given repository name and dataset_id
        """
        try:
            metadata = self._get_metadata(repo_name, dataset_id)
            dataset_source = metadata.get("_source", {}).get("dataset_source")
            return dataset_source
        except Exception:
            print(
                f"Incorrect repo_key{{{repo_name}}} or dataset_id{{{dataset_id}}}. Please check the details"
            )
