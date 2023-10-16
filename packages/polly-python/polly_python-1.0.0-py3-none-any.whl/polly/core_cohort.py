import os
import json
import base64
from polly import helpers
from pathlib import Path
import logging
import pandas as pd
import collections
from polly.errors import (
    InvalidCohortOperationException,
    InvalidParameterException,
    InvalidPathException,
    EmptyCohortException,
    InvalidCohortPathException,
    OutdatedCohortVersion,
)
from polly.constants import OBSOLETE_METADATA_FIELDS, COHORT_VERSION, dot
import shutil
from joblib import Parallel, delayed
from cmapPy.pandasGEXpress.parse import parse
from cmapPy.pandasGEXpress.write_gct import write
from cmapPy.pandasGEXpress.concat import assemble_data
from cmapPy.pandasGEXpress import GCToo


class CohortFileStandard:
    """
    The Class responsible for Encapsulating Core Cohort Functionalities.
    """

    def __init__(self) -> None:
        self._cohort_details = None

    def load_cohort(self, local_path: str):
        """
        Function to load an existing cohort into an object.
        Once loaded, the functions described in the documentation can be used for the object where the cohort is loaded.
        Args:
            | local_path(str): local path of the cohort
        Returns:
            | A confirmation message on instantiation of the cohort
        """
        if not os.path.exists(local_path):
            raise InvalidPathException(local_path)
        file_meta = helpers.make_path(local_path, "cohort.meta")
        if not os.path.exists(file_meta):
            raise InvalidCohortPathException
        file = open(file_meta, "r")
        byte = file.read()
        file.close()
        data = base64.b64decode((byte))
        str_data = data.decode("utf-8")
        json_data = json.loads(str_data)
        version = json_data.get("version")
        if version != COHORT_VERSION:
            raise OutdatedCohortVersion(COHORT_VERSION)
        logging.basicConfig(level=logging.INFO)
        logging.info("Cohort Loaded !")
        self._cohort_details = json_data

    def summarize_cohort(self, cohort_path):
        """
        Function to return metadata and summary of a cohort
        Returns:
            | A tuple with the first value as cohort metadata information (name, description and number of dataset(s)
              or sample(s) in the cohort) and the second value as dataframe containing the source, dataset_id or sample_id
              and data type available in the cohort.
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        meta_details = self._get_metadetails(cohort_path)
        df_details = None
        if "entity_type" not in self._cohort_details:
            df_details = self._get_single_df()
            return meta_details, df_details
        if self._cohort_details.get("entity_type") == "dataset":
            df_details = self._get_single_df()
        else:
            df_details = self._get_multiple_df()
        return meta_details, df_details

    def _get_metadetails(self, cohort_path) -> dict:
        """
        Function to return metadata details of a cohort
        """
        meta_dict = {}
        folder_name = os.path.basename(cohort_path)
        cohort_name = folder_name.split(".")[0]
        meta_dict["cohort_name"] = cohort_name
        meta_details = ["description", "number_of_datasets"]
        for key, value in self._cohort_details.items():
            if key.lower() in meta_details:
                meta_dict[key] = value
        return meta_dict

    def _get_single_df(self) -> pd.DataFrame:
        """
        Function to return cohort summary in a dataframe
        """
        df_dict = {"source_omixatlas": [], "datatype": [], "dataset_id": []}
        dataset_list = list(self._cohort_details["entity_id"].keys())
        for entity in dataset_list:
            omixatlas = self._cohort_details.get("entity_id", {}).get(entity, {})[0]
            data_type = self._cohort_details.get("entity_id", {}).get(entity, {})[1]
            df_dict["dataset_id"].append(entity)
            df_dict["source_omixatlas"].append(omixatlas)
            df_dict["datatype"].append(data_type)
        dataframe = pd.DataFrame.from_dict(df_dict)
        return dataframe

    def _get_multiple_df(self) -> pd.DataFrame:
        """
        Function to return cohort summary in a dataframe
        """
        df_dict = {
            "source_omixatlas": [],
            "datatype": [],
            "dataset_id": [],
            "sample_id": [],
            "number_of_samples": [],
        }
        dataset_list = list(self._cohort_details["entity_id"].keys())
        for entity in dataset_list:
            omixatlas = self._cohort_details.get("entity_id", {}).get(entity, {})[0]
            data_type = self._cohort_details.get("entity_id", {}).get(entity, {})[1]
            sample_id = (
                self._cohort_details.get("source_omixatlas", {})
                .get(omixatlas, {})
                .get(entity)
            )
            df_dict["dataset_id"].append(entity)
            df_dict["source_omixatlas"].append(omixatlas)
            df_dict["datatype"].append(data_type)
            df_dict["sample_id"].append(sample_id)
            df_dict["number_of_samples"].append(len(sample_id))
        dataframe = pd.DataFrame.from_dict(df_dict)
        return dataframe

    def _read_gcts(self, dataset_ids: list, file_path: str) -> list:
        gct_files = [
            f"{file_path}/{self._cohort_details.get('entity_id',{}).get(dataset_id)[0]}_{dataset_id}.gct"
            for dataset_id in dataset_ids
        ]
        results_gct = Parallel(n_jobs=len(gct_files))(
            delayed(parse)(gct_file) for gct_file in gct_files
        )
        return results_gct

    def merge_single_sample_metadata(self, cohort_path: str):
        """
        Function to merge the sample level metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged metadata for analysis.
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        sample_list = list(self._cohort_details["entity_id"].keys())
        if len(sample_list) == 0:
            raise EmptyCohortException
        results_gct = self._read_gcts(sample_list, cohort_path)
        for i in range(0, len(results_gct)):
            df = results_gct[i].col_metadata_df
            index_l = len(df.index)
            new_dataset = [sample_list[i]] * index_l
            results_gct[i].col_metadata_df.insert(
                loc=0, column="dataset_id", value=new_dataset
            )
        All_Metadata = pd.concat([i.col_metadata_df for i in results_gct])
        return All_Metadata

    def merge_single_data_matrix(self, cohort_path: str) -> pd.DataFrame:
        """
        Function to merge the data-matrix level metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged data for analysis.
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        sample_list = list(self._cohort_details["entity_id"].keys())
        if len(sample_list) == 0:
            raise EmptyCohortException
        results_gct = self._read_gcts(sample_list, cohort_path)
        All_data_matrix = assemble_data(
            [i.data_df for i in results_gct], concat_direction="horiz"
        )
        return All_data_matrix

    def merge_dataset_metadata(self, cohort_path: str) -> pd.DataFrame:
        """
        Function to merge the dataset level metadata from all the jpco files in a cohort.
        Returns:
            | A pandas dataframe containing the merged data for analysis.
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        entity_list = list(self._cohort_details["entity_id"].keys())
        if len(entity_list) == 0:
            raise EmptyCohortException
        jpco_files = [
            f"{cohort_path}/{self._cohort_details.get('entity_id',{}).get(entity_id)[0]}_{entity_id}.jpco"
            for entity_id in entity_list
        ]
        df_dict = []
        for files in jpco_files:
            with open(files, "r") as infile:
                temp_df = json.load(infile)
                df_dict.append(temp_df["_source"])
        df = pd.json_normalize(df_dict)
        first_column = df.pop("dataset_id")
        df.insert(loc=0, column="dataset_id", value=first_column)
        for col in OBSOLETE_METADATA_FIELDS:
            if col in df.columns:
                del df[col]
        return df

    def merge_feature_metadata(self, cohort_path) -> pd.DataFrame:
        """
        Function to merge the feature level metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged data for analysis.
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        sample_list = list(self._cohort_details["entity_id"].keys())
        if len(sample_list) == 0:
            raise EmptyCohortException
        results_gct = self._read_gcts(sample_list, cohort_path)
        for i in range(0, len(results_gct)):
            df = results_gct[i].row_metadata_df
            index_l = len(df.index)
            new_dataset = [sample_list[i]] * index_l
            results_gct[i].row_metadata_df.insert(
                loc=0, column="dataset_id", value=new_dataset
            )
        All_Metadata = pd.concat([i.row_metadata_df for i in results_gct])
        return All_Metadata

    def merge_multiple_sample_metadata(self, cohort_path):
        """
        Function to merge the sample level metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged metadata for analysis.
        """
        sample_list = list(self._cohort_details["entity_id"].keys())
        results_gct = self._read_gcts(sample_list, cohort_path)
        oa_list = []
        for i in sample_list:
            omixatlas = self._cohort_details.get("entity_id", {}).get(i, {})[0]
            oa_list.append(omixatlas)
        new_df_list = []
        for i in range(0, len(results_gct)):
            omixatlas_details = self._cohort_details.get("source_omixatlas")
            sample_details = omixatlas_details[oa_list[i]][sample_list[i]]
            df = results_gct[i].col_metadata_df
            new_df = df.loc[sample_details]
            new_df_list.append(new_df)
        All_Metadata = pd.concat([i for i in new_df_list])
        return All_Metadata

    def merge_multiple_data_matrix(self, cohort_path: str) -> pd.DataFrame:
        """
        Function to merge the data-matrix level metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged data for analysis.
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        sample_list = list(self._cohort_details["entity_id"].keys())
        if len(sample_list) == 0:
            raise EmptyCohortException
        results_gct = self._read_gcts(sample_list, cohort_path)
        oa_list = []
        for i in sample_list:
            omixatlas = self._cohort_details.get("entity_id", {}).get(i, {})[0]
            oa_list.append(omixatlas)
        new_df_list = []
        for i in range(0, len(results_gct)):
            omixatlas_details = self._cohort_details.get("source_omixatlas")
            sample_details = omixatlas_details[oa_list[i]][sample_list[i]]
            df = results_gct[i].data_df
            ripped_df = df[sample_details]
            new_df_list.append(ripped_df)
        All_data_matrix = pd.concat([i for i in new_df_list])
        return All_data_matrix

    def edit_cohort(self, new_cohort_name, new_description, cohort_path):
        returned_path_name = None
        # calling functions to edit description and then cohort name
        if new_description:
            self._edit_cohort_description(cohort_path, new_description)
        if new_cohort_name:
            returned_path_name = self._edit_cohort_name(cohort_path, new_cohort_name)
        return returned_path_name

    def _edit_cohort_name(self, cohort_path, new_cohort_name: str):
        """
        Function to edit cohort name
        """
        if not (new_cohort_name and isinstance(new_cohort_name, str)):
            return
        if dot in new_cohort_name:
            logging.error("The cohort name is not valid. Please try again.")
            return
        p = Path(cohort_path)
        parent = p.parent
        str_parent = str(parent.resolve())
        new_path = helpers.make_path(str_parent, f"{new_cohort_name}.pco")
        existing_path = cohort_path
        os.rename(existing_path, new_path)
        logging.basicConfig(level=logging.INFO)
        logging.info("Cohort Name Updated!")
        return new_path

    def _edit_cohort_description(self, cohort_path: str, new_description: str):
        """
        Function to edit cohort description
        """
        if not (new_description and isinstance(new_description, str)):
            return
        meta_path = helpers.make_path(cohort_path, "cohort.meta")
        json_data = None
        with open(meta_path, "r+b") as openfile:
            byte = openfile.read()
            data = base64.b64decode((byte))
            json_data = json.loads(data.decode("utf-8"))
            json_data["description"] = new_description
            input = json.dumps(json_data)
            encoded_data = base64.b64encode(input.encode("utf-8"))
            openfile.seek(0)
            openfile.write(encoded_data)
            openfile.truncate()
        logging.basicConfig(level=logging.INFO)
        logging.info("Cohort Description Updated!")
        self._cohort_details = json_data

    def is_valid(self, cohort_path: str) -> bool:
        """
        This function is used to check if a cohort is valid or not.
        Returns:
            | A boolean result based on the validity of the cohort.
        """
        if not os.path.exists(cohort_path):
            raise InvalidPathException
        meta_path = helpers.make_path(cohort_path, "cohort.meta")
        if not os.path.exists(meta_path):
            return False
        sample_list = list(self._cohort_details["entity_id"].keys())
        if len(sample_list) == 0:
            return True
        for sample in sample_list:
            omixatlas = self._cohort_details.get("entity_id", {}).get(sample)[0]
            gct_path = f"{cohort_path}/{omixatlas}_{sample}.gct"
            jpco_path = f"{cohort_path}/{omixatlas}_{sample}.jpco"
            if not (os.path.exists(gct_path) and os.path.exists(jpco_path)):
                return False
        return True

    def remove_single_from_cohort(self, cohort_path: str, dataset_id: list) -> None:
        """
        This function is used for removing dataset_id(s) from a cohort
        Args:
            | entity_id(list): list of dataset_id or sample_id to be removed from the cohort.
        Returns:
            | A confirmation message on removal of dataset_id or sample_id from cohort.
        """
        if not (dataset_id and isinstance(dataset_id, list)):
            raise InvalidParameterException("dataset_id")
        dataset_count = 0
        verified_dataset = []
        file_meta = helpers.make_path(cohort_path, "cohort.meta")
        dataset_id = list(set(dataset_id))
        json_data = None
        with open(file_meta, "r+b") as openfile:
            byte = openfile.read()
            data = base64.b64decode((byte))
            json_data = json.loads(data.decode("utf-8"))
            dataset_id_metadata = list(json_data["entity_id"].keys())
            for dataset in dataset_id:
                if dataset not in dataset_id_metadata:
                    logging.basicConfig(level=logging.INFO)
                    logging.info(f"Dataset Id - {dataset} not present in the Cohort.")
                    continue
                dataset_count += 1
                verified_dataset.append(dataset)
                omixatlas = json_data.get("entity_id", {}).get(dataset)[0]
                gct_path = f"{cohort_path}/{omixatlas}_{dataset}.gct"
                json_path = f"{cohort_path}/{omixatlas}_{dataset}.jpco"
                os.remove(gct_path)
                os.remove(json_path)
                del json_data.get("entity_id")[dataset]
                json_data.get("source_omixatlas").get(omixatlas).remove(dataset)
            omixatlas_dict = json_data.get("source_omixatlas")
            empty_keys = []
            for key, value in omixatlas_dict.items():
                if value == []:
                    empty_keys.append(key)
            for key in empty_keys:
                del omixatlas_dict[key]
            json_data["number_of_datasets"] -= dataset_count
            json_data["source_omixatlas"] = omixatlas_dict
            if not bool(json_data.get("entity_id")):
                if "entity_type" in json_data:
                    del json_data["entity_type"]
            input = json.dumps(json_data)
            encoded_data = base64.b64encode(input.encode("utf-8"))
            openfile.seek(0)
            openfile.write(encoded_data)
            openfile.truncate()
        logging.basicConfig(level=logging.INFO)
        logging.info(f"'{dataset_count}' dataset/s removed from Cohort!")
        self._cohort_details = json_data

    def remove_multiple_from_cohort(self, cohort_path, dataset_id: str, sample_id=[]):
        """
        This function is used for removing dataset_id or sample_id from a cohort
        Args:
            | entity_id(list): list of dataset_id or sample_id to be removed from the cohort.
        Returns:
            | A confirmation message on removal of dataset_id or sample_id from cohort.
        """
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        file_meta = helpers.make_path(cohort_path, "cohort.meta")
        json_data = None
        with open(file_meta, "r+b") as openfile:
            byte = openfile.read()
            data = base64.b64decode((byte))
            json_data = json.loads(data.decode("utf-8"))
            dataset_id_metadata = list(json_data["entity_id"].keys())
            if dataset_id not in dataset_id_metadata:
                logging.basicConfig(level=logging.INFO)
                logging.info(f"Dataset Id - {dataset_id} not present in the Cohort.")
            else:
                source_omixatlas = json_data.get("source_omixatlas")
                omixatlas = json_data.get("entity_id", {}).get(dataset_id)[0]
                list_of_samples = source_omixatlas.get(omixatlas, {}).get(dataset_id)
                if len(sample_id) > 0:
                    sample_id = list(set(sample_id))
                    new_list_of_samples = [
                        x for x in list_of_samples if x not in sample_id
                    ]
                    if len(new_list_of_samples) != 0:
                        if collections.Counter(
                            new_list_of_samples
                        ) == collections.Counter(list_of_samples):
                            print("Invalid Samples to remove! ")
                        else:
                            json_data.get("source_omixatlas").get(omixatlas, {})[
                                dataset_id
                            ] = new_list_of_samples
                            print("Samples removed successfully!")
                    else:
                        json_data = self._remove_dataset(
                            dataset_id, json_data, cohort_path
                        )
                else:
                    json_data = self._remove_dataset(dataset_id, json_data, cohort_path)
                input = json.dumps(json_data)
                encoded_data = base64.b64encode(input.encode("utf-8"))
                openfile.seek(0)
                openfile.write(encoded_data)
                openfile.truncate()
        self._cohort_details = json_data

    def _remove_dataset(self, dataset_id: str, json_data: dict, cohort_path: str):
        omixatlas = json_data.get("entity_id", {}).get(dataset_id)[0]
        gct_path = f"{cohort_path}/{omixatlas}_{dataset_id}.gct"
        json_path = f"{cohort_path}/{omixatlas}_{dataset_id}.jpco"
        os.remove(gct_path)
        os.remove(json_path)
        del json_data.get("entity_id")[dataset_id]
        json_data.get("source_omixatlas").get(omixatlas).pop(dataset_id)
        omixatlas_dict = json_data.get("source_omixatlas")
        empty_keys = []
        for key, value in omixatlas_dict.items():
            if value == {}:
                empty_keys.append(key)
        for key in empty_keys:
            del omixatlas_dict[key]
        json_data["number_of_datasets"] -= 1
        json_data["source_omixatlas"] = omixatlas_dict
        if not bool(json_data.get("entity_id")):
            if "entity_type" in json_data:
                del json_data["entity_type"]
        logging.basicConfig(level=logging.INFO)
        logging.info(" 1 dataset removed from Cohort!")
        return json_data

    def _update_metadata_single(
        self, repo_name, entity_type, dataset_id, deleted_id, file_meta, dataset_tuple
    ):
        json_data = None
        with open(file_meta, "r+b") as openfile:
            byte = openfile.read()
            data = base64.b64decode((byte))
            json_data = json.loads(data.decode("utf-8"))
            source_omixatlas = json_data.get("source_omixatlas")
            if "entity_type" not in json_data:
                json_data["entity_type"] = entity_type
            if repo_name not in source_omixatlas:
                source_omixatlas[repo_name] = dataset_id
            else:
                [source_omixatlas[repo_name].append(i) for i in dataset_id]
            for i in range(0, len(dataset_id)):
                json_data["entity_id"][dataset_id[i]] = dataset_tuple[i]
                json_data["number_of_datasets"] += 1
            input = json.dumps(json_data)
            encoded_data = base64.b64encode(input.encode("utf-8"))
            openfile.seek(0)
            openfile.write(encoded_data)
            openfile.truncate()
        logging.basicConfig(level=logging.INFO)
        if deleted_id:
            logging.info("The following entities were not added : ")
            for id in deleted_id:
                print(f"{id}\n")
        logging.info(f"'{len(dataset_id)}' dataset/s added to Cohort!")
        return json_data

    def _update_metadata_multiple(
        self,
        repo_name,
        entity_type,
        dataset_id,
        sample_id,
        download_flag,
        file_meta,
        status_sample_id,
        dataset_tuple,
    ):
        json_data = None
        with open(file_meta, "r+b") as openfile:
            byte = openfile.read()
            data = base64.b64decode((byte))
            json_data = json.loads(data.decode("utf-8"))
            source_omixatlas = json_data.get("source_omixatlas")
            list_of_samples = []
            if "entity_type" not in json_data:
                json_data["entity_type"] = entity_type
            if repo_name not in source_omixatlas:
                source_omixatlas[repo_name] = {}
            elif dataset_id in source_omixatlas.get(repo_name):
                list_of_samples = source_omixatlas.get(repo_name, {}).get(dataset_id)
            sample_added = 0
            for i in range(0, len(sample_id)):
                if status_sample_id[i] and sample_id[i] not in list_of_samples:
                    sample_added += 1
                    list_of_samples.append(sample_id[i])
            source_omixatlas.get(repo_name, {})[dataset_id] = list_of_samples
            json_data["entity_id"][dataset_id] = dataset_tuple
            if download_flag:
                json_data["number_of_datasets"] += 1
            json_data["source_omixatlas"] = source_omixatlas
            input = json.dumps(json_data)
            encoded_data = base64.b64encode(input.encode("utf-8"))
            openfile.seek(0)
            openfile.write(encoded_data)
            openfile.truncate()
        logging.basicConfig(level=logging.INFO)
        logging.info(f"'{sample_added}' sample/s added to Cohort!")
        return json_data

    def _rollback_files(
        self,
        status_gct: list,
        status_jpco: list,
        repo_name: str,
        local_path: str,
        dataset_id: list,
    ) -> tuple:
        """
        Returns a list of dataset_ids and deleted_ids
        """
        deleted_id = []
        for i in status_gct:
            if i != 0:
                gct_file = f"{repo_name}_{i}.gct"
                gct_path = helpers.make_path(local_path, gct_file)
                jpco_file = f"{repo_name}_{i}.jpco"
                jpco_path = helpers.make_path(local_path, jpco_file)
                if os.path.exists(gct_path):
                    os.remove(gct_path)
                if os.path.exists(jpco_path):
                    os.remove(jpco_path)
                deleted_id.append(i)
                dataset_id.remove(i)
        for i in status_jpco:
            if i != 0 and i not in deleted_id:
                gct_file = f"{repo_name}_{i}.gct"
                gct_path = helpers.make_path(local_path, gct_file)
                jpco_file = f"{repo_name}_{i}.jpco"
                jpco_path = helpers.make_path(local_path, jpco_file)
                if os.path.exists(gct_path):
                    os.remove(gct_path)
                if os.path.exists(jpco_path):
                    os.remove(jpco_path)
                deleted_id.append(i)
                dataset_id.remove(i)
        return dataset_id, deleted_id

    def delete_cohort(self, cohort_path: str) -> None:
        """
        This function is used to delete a cohort.
        Returns:
            | A confirmation message on deletion of cohort
        """
        shutil.rmtree(cohort_path, ignore_errors=True)
        logging.basicConfig(level=logging.INFO)
        logging.info("Cohort Deleted Successfuly!")
        self._cohort_details = None

    def _rename_samples(self, dataset_id: str, gct_object: GCToo) -> GCToo:
        """
        Adds dataset_id as prefix to the sample names (cids) in the gct object
        """
        gct_object.data_df.columns = [
            dataset_id + "_" + sample for sample in gct_object.data_df.columns
        ]
        gct_object.col_metadata_df.index = [
            [dataset_id + "_" + sample for sample in gct_object.col_metadata_df.index]
        ]
        return gct_object

    def merge_gcts(
        self, entity_type: str, cohort_path: str, file_name: str, file_path: str
    ) -> None:
        """
        Merge the input gcts together to create one gct object. Only the features(genes) common to all the gcts are retained.
        """
        dataset_ids = list(self._cohort_details["entity_id"].keys())
        omixatlas_details = self._cohort_details.get("source_omixatlas")
        gct_files = [
            f"{cohort_path}/{self._cohort_details.get('entity_id',{}).get(dataset_id)[0]}_{dataset_id}.gct"
            for dataset_id in dataset_ids
        ]
        gct_objects = {
            dataset_id: parse(gct_file)
            for dataset_id, gct_file in zip(dataset_ids, gct_files)
        }
        # Creating a dict for dataset_id to samples mapping with dataset_id prefixed
        dataset_sample_mapping = {}
        # Collecting samples by differentiating between entity_types of cohort
        if entity_type == "sample":
            # Cohort contains repositories with multiple mapped datasets
            for dataset in dataset_ids:
                omixatlas = self._cohort_details.get("entity_id", {}).get(dataset, {})[
                    0
                ]
                samples = omixatlas_details.get(omixatlas, {}).get(dataset)
                dataset_sample_mapping[dataset] = [
                    f"{dataset}_{sample}" for sample in samples
                ]
        else:
            # Cohort contains repositories with single mapped datasets
            for dataset in dataset_ids:
                samples = list(gct_objects[dataset].col_metadata_df.index)
                dataset_sample_mapping[dataset] = [
                    f"{dataset}_{sample}" for sample in samples
                ]
        # Dictionaries for parsed data
        data_df_dict = {}
        col_metadata_dict = {}
        for dataset_id in dataset_ids:
            # Rename all samples for each gct and add dataset_id as a column to col metadata of each gct object
            gct_objects[dataset_id] = self._rename_samples(
                dataset_id, gct_objects[dataset_id]
            )
            gct_objects[dataset_id].col_metadata_df["dataset_id"] = dataset_id
            # Separating data_df and col_metadata_df, with tailored index and columns according to samples
            samples = dataset_sample_mapping[dataset_id]
            sampled_data_df = gct_objects[dataset_id].data_df[samples]
            sampled_col_metadata_df = gct_objects[dataset_id].col_metadata_df.loc[
                samples
            ]
            # Step to ensure index is a proper list
            sampled_col_metadata_df.index = samples
            data_df_dict[dataset_id] = sampled_data_df
            col_metadata_dict[dataset_id] = sampled_col_metadata_df

        if len(dataset_ids) == 1:
            # No need to merge as only one dataset present
            merged_data_df = data_df_dict[dataset_ids[0]]
            merged_col_metadata_df = col_metadata_dict[dataset_ids[0]]
            merged_row_metadata_df = gct_objects[dataset_ids[0]].row_metadata_df.loc[
                merged_data_df.index
            ]
        else:
            merged_data_df = pd.merge(
                data_df_dict[dataset_ids[0]],
                data_df_dict[dataset_ids[1]],
                left_index=True,
                right_index=True,
            )
            merged_col_metadata_df = pd.concat(
                [
                    col_metadata_dict[dataset_ids[0]],
                    col_metadata_dict[dataset_ids[1]],
                ],
                axis=0,
            )
            if len(dataset_ids) > 2:
                for dataset_id in dataset_ids[2:]:
                    merged_data_df = pd.merge(
                        merged_data_df,
                        data_df_dict[dataset_id],
                        left_index=True,
                        right_index=True,
                    )
                    merged_col_metadata_df = pd.concat(
                        [merged_col_metadata_df, col_metadata_dict[dataset_id]],
                        axis=0,
                    )
            merged_row_metadata_df = gct_objects[dataset_ids[0]].row_metadata_df.loc[
                merged_data_df.index
            ]
        merged_gct_object = GCToo.GCToo(
            data_df=merged_data_df,
            row_metadata_df=merged_row_metadata_df,
            col_metadata_df=merged_col_metadata_df,
        )
        write(merged_gct_object, helpers.make_path(file_path, file_name))
