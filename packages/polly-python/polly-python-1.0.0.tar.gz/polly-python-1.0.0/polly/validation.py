from polly.help import example
from polly.auth import Polly
from polly import helpers, constants as const
import pandas as pd
import polly.validation_hlpr as validation_hlpr
from polly.tracking import Track

# from polly_validator.validators import dataset_metadata_validator


class Validation:
    """Validation Class for Integrating External Validation Library"""

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

    @Track.track_decorator
    def get_ingestion_configs(
        self, indexing_configs=True, validation_configs=True
    ) -> dict:
        """Return the ingestion configs in dictionary which contain two sections
        i) indexing_configs
        {
            "file_metadata": true/false
            "col_metadata": true/false,
            "row_metadata": true/false,
            "data_required": true/false
        }


        ii) validation_configs
        "validation_check": {
            "dataset": {
                "validate": false/true,
                "scope": "advanced"/"basic",
                "force_ingest": false/true
            },
            "sample": {
                "validate": false/true,
                "scope": "advanced"/"basic",
                "force_ingest": false/true
            }
        }

        Args:
            indexing_configs (bool, optional): Optional parameter(True/False)
            validation_configs (bool, optional): Optional parameter(True/False)


        Returns:
            dict: dictionary returning the ingestion configs in a dictionary
        """

        ingestion_configs = {}

        if indexing_configs:
            indexing_configs_dict = validation_hlpr.get_indexing_configs()
            ingestion_configs.update(indexing_configs_dict)

        if validation_configs:
            dataset_config_dict = validation_hlpr.get_dataset_level_validation_config()
            sample_config_dict = validation_hlpr.get_sample_level_validation_configs()
            ingestion_configs["validation_check"] = {}
            ingestion_configs["validation_check"]["dataset"] = dataset_config_dict
            ingestion_configs["validation_check"]["sample"] = sample_config_dict

        return ingestion_configs

    @Track.track_decorator
    def validate_datasets(
        self, repo_id: int, source_folder_path: dict, schema_config={}
    ) -> pd.DataFrame:
        """Validate the dataset level metadata for datasets to be Ingested
        Args:
            repo_id(int/string): Repo id of OmixAtlas
            source_folder_path(dict): Source folder path of data and metadata files.
            schema_config(dict): source and datatype of the repo schema on which \
            users want to get their data validated
        Returns:
            err_dataset(DataFrame): All the errors
            status_dict(Dictionary): Status of all the Files
        """
        # add method to validate the params
        try:
            self._check_validate_dataset_params(
                repo_id, source_folder_path, schema_config
            )
            repo_id = helpers.make_repo_id_string(repo_id)
            return self._validate_dataset_level_metadata(
                repo_id, source_folder_path, schema_config
            )
        except Exception as err:
            raise err

    def _check_validate_dataset_params(
        self, repo_id: str, source_folder_path: dict, schema_config: dict
    ):
        """Check passed params in validate datasets
        Args:
            repo_id(int/string): Repo id of the repo
            source_folder_path(dict): Source folder path from data and metadata files are fetched
        """
        try:
            helpers.parameter_check_for_repo_id(repo_id)
            validation_hlpr.data_metadata_parameter_check(source_folder_path)
            # if schema config dict is not empty, then only check its params
            # else not needed
            if bool(schema_config):
                validation_hlpr.schema_config_check(schema_config)
        except Exception as err:
            raise err

    def _validate_dataset_level_metadata(
        self, repo_id: str, source_folder_path: dict, schema_config
    ) -> pd.DataFrame:
        """Validate Dataset level metadata
        Args:
            repo_id(int/string): Repo id of OmixAtlas
            source_folder_path(dict): Source folder path of data and metadata files.
            schema_config(dict): source and datatype of the repo schema on which \
            users want to get their data validated
        Returns:
            err_dataset(DataFrame): All the errors
            status_dict(Dictionary): Status of all the Files
        """
        # list of metadata files to validate
        # metadata files grouped in a list
        # grouping is done on validation level parameter
        try:
            # construct dataframe of schema for the repo
            # formatted schema DF based on Input Required by Validation Lib
            # Formatted DF has 2 rows -> Field Name and Type
            # schema_df_dataset = self._construct_df_of_schema(repo_id)

            schema_dict = validation_hlpr.get_dataset_level_schema(
                repo_id, schema_config
            )
            combined_metadata = (
                validation_hlpr.construct_combined_metadata_for_validation(
                    source_folder_path
                )
            )
            # Only run validation if there are files to be validated
            if combined_metadata:
                validation_lib_res = validation_hlpr.validate_datasets(
                    repo_id, schema_dict, combined_metadata
                )
                error_df = helpers.merge_dataframes_from_list(
                    validation_lib_res.get("error")
                )
                status_dict = helpers.merge_dicts_from_list(
                    validation_lib_res.get("status")
                )
                validation_hlpr.create_status_file(
                    status_dict, source_folder_path["metadata"]
                )
                return error_df, status_dict
            else:
                print(const.VALIDATION_NOT_EXECUTED)
        except Exception as err:
            raise err
