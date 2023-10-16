from polly import helpers
from polly.errors import (
    InvalidCohortOperationException,
    InvalidParameterException,
    InvalidRepoException,
    CohortEditException,
    EmptyCohortException,
    InvalidCohortAddition,
    InvalidCohortMergeOperation,
    InvalidPathException,
)
import os
import pandas as pd
from deprecated import deprecated
from polly.bridge_cohort import CohortRepoClass
from polly.core_cohort import CohortFileStandard
from polly import constants as const
from polly.help import example
from polly.auth import Polly
from polly.tracking import Track


class Cohort:
    """
    The Cohort class contains functions which can be used to create cohorts, add or remove samples, \
    merge metadata and data-matrix of samples/datasets in a cohort and edit or delete a cohort.
    Args:
        token (str): Authentication token from polly
    Usage:
        from polly.cohort import Cohort

        cohort = Cohort(token)
    """

    _cohort_info = None
    example = classmethod(example)

    def __init__(self, token=None, env="", default_env="polly") -> None:
        # check if COMPUTE_ENV_VARIABLE present or not
        # if COMPUTE_ENV_VARIABLE, give priority
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        if self._cohort_info is None:
            self._cohort_info = helpers.get_cohort_constants()
        self._cohort_path = None
        self._cohort_details = None
        self.bridge_obj = CohortRepoClass(self.session)
        self.core_obj = CohortFileStandard()

    @Track.track_decorator
    def create_cohort(
        self,
        local_path: str,
        cohort_name: str,
        description: str,
        repo_key=None,
        dataset_id=None,
        sample_id=None,
    ) -> None:
        """
        This function is used to create a cohort. After making Cohort Object you can create cohort.

        Args:
              local_path (str): local path to instantiate the cohort.
              cohort_name (str): identifier name for the cohort.
              description (str): description about the cohort.
              repo_key (str, optional): repo_key(repo_name/repo_id) for the omixatlas \
                from where datasets or samples is to be added.
              dataset_id (list/str, optional): dataset_ids(list,in case of repositories where one dataset has 1 \
                sample) or a dataset_id(str,in case of in case of repository where 1 dataset has many samples)
              sample_id (list, optional): list of samples to be added in cohort, \
                applicable only in case of in case of repository where 1 dataset has many samples.

        Returns:
              A message will be displayed on the status of the operation.

        Raises:
              InvalidParameterException: Empty or Invalid Parameters
              InvalidCohortNameException: The cohort_name does not represent a valid cohort name.
              InvalidPathException: Provided path does not represent a file or a directory.
        """
        self._cohort_path = self.bridge_obj.create_cohort(
            local_path, cohort_name, description
        )
        self._cohort_details = self.bridge_obj._cohort_details
        if repo_key:
            self.add_to_cohort(
                repo_key=repo_key,
                dataset_id=dataset_id,
                sample_id=sample_id,
            )

    @Track.track_decorator
    def add_to_cohort(self, repo_key: str, dataset_id=None, sample_id=None) -> None:
        """
        This function is used to add datasets or samples to a cohort.

        Args:
              repo_key (str): repo_key(repo_name OR repo_id) for the omixatlas where datasets or samples belong.
              dataset_id (list/str): dataset_ids(list,in case of repositories where one dataset has 1 \
                sample) or a dataset_id(str,in case of in case of repository where 1 dataset has many samples)
              sample_id (list, optional): list of samples to be added in cohort, \
                applicable only in case of in case of repository where 1 dataset has many samples.

        Returns:
              A message will be displayed on the status of the operation.

            Raises:
              InvalidParameterException: Empty or Invalid Parameters.
              InvalidCohortOperationException: This operation is not valid as no cohort has been instantiated.
        """
        self.bridge_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if not ((repo_key and dataset_id and sample_id) or (repo_key and dataset_id)):
            raise InvalidParameterException("repo_key dataset_id sample_id")
        repo_name = self.bridge_obj._return_omixatlas_name(repo_key)
        if repo_name not in self._cohort_info:
            raise InvalidRepoException(repo_name)
        cohort_entity_type = self._assign_entity_type(repo_name, dataset_id)
        if "entity_type" in self._cohort_details:
            existing_entity_type = self._cohort_details.get("entity_type")
            if existing_entity_type != cohort_entity_type:
                raise InvalidCohortAddition
        self.bridge_obj._cohort_details = self._cohort_details
        if cohort_entity_type == "dataset":
            self.bridge_obj.add_to_cohort_single(
                self._cohort_path,
                repo_name=repo_name,
                entity_id=dataset_id,
                entity_type=cohort_entity_type,
            )
        else:
            self.bridge_obj.add_to_cohort_multiple(
                self._cohort_path,
                repo_name=repo_name,
                dataset_id=dataset_id,
                sample_id=sample_id,
                entity_type=cohort_entity_type,
            )
        self._cohort_details = self.bridge_obj._cohort_details

    @Track.track_decorator
    def remove_from_cohort(self, dataset_id=None, sample_id=[]) -> None:
        """
        This function is used for removing datasets or samples from a cohort.

        Args:
              dataset_id (list/str): dataset_ids(list,in case of repositories where one dataset has 1 \
                sample) or a dataset_id(str,in case of in case of repository where 1 dataset has many samples)
              sample_id (list, optional): list of samples to be added in cohort, \
                applicable only in case of in case of repository where 1 dataset has many samples.

        Returns:
              A message will be displayed on the status of the operation.

        Raises:
              InvalidParameterException: Empty or Invalid Parameters
              InvalidCohortOperationException: This operation is not valid as no cohort has been instantiated.
        """
        self.core_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if "entity_type" not in self._cohort_details:
            raise EmptyCohortException
        entity_type = self._cohort_details.get("entity_type")
        if entity_type == "dataset":
            self.core_obj.remove_single_from_cohort(self._cohort_path, dataset_id)
        else:
            self.core_obj.remove_multiple_from_cohort(
                self._cohort_path, dataset_id, sample_id
            )
        self._cohort_details = self.core_obj._cohort_details

    @Track.track_decorator
    def merge_data(self, data_level: str):
        """
        Function to merge metadata (dataset,sample and feature level) or data-matrix of all the samples/datasets in the cohort.

        Args:
                data_level (str): identifier to specify the data to be merged - "dataset", "sample", "feature" or "data_matrix"

        Returns:
                A pandas dataframe containing the merged data which is ready for analysis
        """
        self.core_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if not (data_level and isinstance(data_level, str)):
            raise InvalidParameterException("data_level")
        if "entity_type" not in self._cohort_details:
            raise EmptyCohortException
        if not (data_level and isinstance(data_level, str)):
            raise InvalidParameterException("data_level")
        if data_level == "sample":
            sample_df = self._merge_sample_metadata()
            return sample_df
        if data_level == "dataset":
            dataset_df = self._merge_dataset_metadata()
            return dataset_df
        if data_level == "data_matrix":
            datamatrix_df = self._merge_data_matrix()
            return datamatrix_df
        if data_level == "feature":
            feature_df = self._merge_feature_metadata()
            return feature_df
        raise InvalidCohortMergeOperation

    @deprecated(reason="use function merge_data")
    def _merge_sample_metadata(self) -> pd.DataFrame:
        """
        Function to merge the sample level metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged metadata for analysis.

        :meta private:
        """
        self.core_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if "entity_type" not in self._cohort_details:
            raise EmptyCohortException
        entity_type = self._cohort_details.get("entity_type")
        if entity_type == "sample":
            return self.core_obj.merge_multiple_sample_metadata(self._cohort_path)
        else:
            return self.core_obj.merge_single_sample_metadata(self._cohort_path)

    @Track.track_decorator
    def is_valid(self) -> bool:
        """
        This function is used to check the validity of a cohort.

        Returns:
                A boolean result based on the validity of the cohort.

        Raises:
                InvalidPathException: Cohort path does not represent a file or a directory.
                InvalidCohortOperationException: This operation is not valid as no cohort has been instantiated.
        """
        self.core_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        return self.core_obj.is_valid(self._cohort_path)

    @deprecated(reason="use function merge_data")
    def _merge_feature_metadata(self) -> pd.DataFrame:
        """
        Function to merge the feature level metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged metadata for analysis.

        :meta private:
        """
        self.core_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if "entity_type" not in self._cohort_details:
            raise EmptyCohortException
        return self.core_obj.merge_feature_metadata(self._cohort_path)

    @deprecated(reason="use function merge_data")
    def _merge_dataset_metadata(self) -> pd.DataFrame:
        """
        Function to merge the dataset level metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged metadata for analysis.

        :meta private:
        """
        self.core_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if "entity_type" not in self._cohort_details:
            raise EmptyCohortException
        return self.core_obj.merge_dataset_metadata(self._cohort_path)

    @deprecated(reason="use function merge_data")
    def _merge_data_matrix(self) -> pd.DataFrame:
        """
        Function to merge the data matrix metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged metadata for analysis.

        :meta private:
        """
        self.core_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if "entity_type" not in self._cohort_details:
            raise EmptyCohortException
        entity_type = self._cohort_details.get("entity_type")
        if entity_type == "sample":
            return self.core_obj.merge_multiple_data_matrix(self._cohort_path)
        else:
            return self.core_obj.merge_single_data_matrix(self._cohort_path)

    @Track.track_decorator
    def load_cohort(self, local_path: str):
        """
        Function to load an existing cohort into an object.
        Once loaded, the functions described in the documentation can be used for the object where the cohort is loaded.

        Args:
                    local_path (str): local path of the cohort.

        Returns:
                    A confirmation message on instantiation of the cohort.
        Raises:
                    InvalidPathException: This path does not represent a file or a directory.
                    InvalidCohortPathException: This path does not represent a Cohort.

        """
        self.core_obj.load_cohort(local_path)
        self._cohort_path = local_path
        self._cohort_details = self.core_obj._cohort_details

    @Track.track_decorator
    def edit_cohort(self, new_cohort_name=None, new_description=None):
        """
        This function is used to edit the cohort level metadata such as cohort name and description.
        Atleast one of the argument should be present.
        Args:
                    new_cohort_name (str): new identifier name for the cohort.
                    new_description (str): new description about the cohort.

            Returns:
                    A confirmation message on updation of cohort.

            Raises:
                    InvalidCohortOperationException: This operation is not valid as no cohort has been instantiated.
                    CohortEditException: No parameter specified for editing in cohort
        """
        self.core_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if new_cohort_name is None and new_description is None:
            raise CohortEditException
        new_path = self.core_obj.edit_cohort(
            new_cohort_name, new_description, self._cohort_path
        )
        if new_path:
            self._cohort_path = new_path
        self._cohort_details = self.core_obj._cohort_details

    @Track.track_decorator
    def summarize_cohort(self):
        """
        Function to return cohort level metadata and dataframe with datasets or samples added in the cohort.

        Returns:
              A tuple with the first value as cohort metadata information
              (name, description and number of dataset(s) or sample(s) in the cohort) and the second value
              as dataframe containing the source, dataset_id/sample_id and data type available in the cohort.

            Raises:
              InvalidCohortOperationException: This operation is not valid as no cohort has been instantiated.
        """
        self.core_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        return self.core_obj.summarize_cohort(self._cohort_path)

    @Track.track_decorator
    def delete_cohort(self) -> None:
        """
        This function is used to delete a cohort.
        Returns:
            A confirmation message on deletion of cohort
        """
        self.core_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        self.core_obj.delete_cohort(self._cohort_path)
        self.bridge_obj._cohort_details = self.core_obj._cohort_details
        self._cohort_details = self.core_obj._cohort_details
        self._cohort_path = None

    def _assign_entity_type(self, repo_name: str, dataset_id: str) -> str:
        """
        Function to return entity type
        Input: repo_name(str) and dataset_id(str or list)
        Returns: Entity_type('dataset' for single mapped repositories,\
            'sample' for multiple mapped repositories.)
        """
        for repo, dict in self._cohort_info.items():
            if repo_name == repo:
                if dict["file_structure"] == "single":
                    cohort_entity_type = "dataset"
                elif dict["file_structure"] == "multiple":
                    cohort_entity_type = "sample"
                else:
                    cohort_entity_type = self.bridge_obj._get_entity_type(
                        repo_name, dataset_id, self._cohort_info
                    )
        return cohort_entity_type

    @Track.track_decorator
    def create_merged_gct(self, file_path: str, file_name="") -> None:
        """
          This function is used to merge all the gct files in a cohort into a single gct file.

        Args:
                    file_path (str): the system path where the gct file is to be written.
                    file_name (str, optional): Identifier for the merged file name, cohort name will be used by default.
        """
        self.core_obj._cohort_details = self._cohort_details
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if "entity_type" not in self._cohort_details:
            raise EmptyCohortException
        if not isinstance(file_name, str):
            raise InvalidParameterException("file_name")
        isExists = os.path.exists(file_path)
        if not isExists:
            raise InvalidPathException
        if file_name:
            if not isinstance(file_name, str):
                raise InvalidParameterException("file_name")
            file_name = f"{file_name}.gct"
        else:
            # Fetching cohort name to be used as the file name
            cohort_info = self.summarize_cohort()
            cohort_name = cohort_info[0].get("cohort_name")
            file_name = f"{cohort_name}.gct"
        entity_type = self._cohort_details.get("entity_type")
        self.core_obj.merge_gcts(entity_type, self._cohort_path, file_name, file_path)
