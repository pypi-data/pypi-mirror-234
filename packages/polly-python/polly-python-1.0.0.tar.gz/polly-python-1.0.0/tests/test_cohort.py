from polly import cohort
from polly.auth import Polly
import os

key = "POLLY_API_KEY"
token = os.getenv(key)
cohort_name_single = "sample_single_cohort"
cohort_name_multiple = "sample_multiple_cohort"
edited_cohort_name_single = "new_sample_single_cohort"
description = "Description for Cohort."
single_repository = "tcga"
multiple_repository = "metabolomics"
dataset_id_single = "ACC_Mutation_TCGA-OR-A5J2-01A-11D-A29I-10"
dataset_id_multiple = "MTBLS105_m_mtbls105_GC_SIM_mass_spectrometry"


def test_obj_initialised():
    Polly.auth(token)
    assert cohort.Cohort() is not None
    assert cohort.Cohort(token) is not None
    assert Polly.get_session(token) is not None


def test_create_cohort_single():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = os.getcwd()
    assert obj.create_cohort(cohort_path, cohort_name_single, description) is None
    assert obj._cohort_details is not None


def test_load_cohort_single():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_single}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None


def test_add_to_cohort_single():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_single}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    assert obj.add_to_cohort(single_repository, [dataset_id_single]) is None


def test_summarize_cohort_single():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_single}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    a, b = obj.summarize_cohort()
    assert a is not None
    assert b is not None


def test_merge_cohort_single():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_single}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    assert obj.merge_data("sample") is not None
    assert obj.merge_data("feature") is not None
    assert obj.merge_data("dataset") is not None
    assert obj.merge_data("data_matrix") is not None


def test_is_valid_single():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_single}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    assert obj.is_valid() is True


def test_single_create_merged_gct():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_single}.pco"
    obj.load_cohort(cohort_path)
    file_path = os.getcwd()
    file_name = "single_cohort"
    assert obj.create_merged_gct(file_path) is None
    assert obj.create_merged_gct(file_path, file_name) is None
    os.remove(f"{file_path}/{file_name}.gct")
    os.remove(f"{file_path}/{cohort_name_single}.gct")


def test_remove_from_cohort_single():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_single}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    dataset_id_list = [dataset_id_single]
    assert obj.remove_from_cohort(dataset_id_list) is None


def test_edit_cohort_single():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_single}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    assert obj.edit_cohort(new_cohort_name=edited_cohort_name_single) is None


def test_delete_cohort_single():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{edited_cohort_name_single}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    obj.delete_cohort()
    assert obj._cohort_details is None


def test_create_cohort_multiple():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = os.getcwd()
    assert (
        obj.create_cohort(
            cohort_path,
            cohort_name_multiple,
            description,
        )
        is None
    )
    assert obj._cohort_details is not None


def test_load_cohort_multiple():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_multiple}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None


def test_add_to_cohort_multiple():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_multiple}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    assert obj.add_to_cohort(multiple_repository, dataset_id_multiple) is None


def test_summarize_cohort_multiple():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_multiple}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    a, b = obj.summarize_cohort()
    assert a is not None
    assert b is not None


def test_merge_cohort_multiple():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_multiple}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    assert obj.merge_data("sample") is not None
    assert obj.merge_data("feature") is not None
    assert obj.merge_data("dataset") is not None
    assert obj.merge_data("data_matrix") is not None


def test_is_valid_multiple():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_multiple}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    assert obj.is_valid() is True


def test_multiple_create_merged_gct():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_multiple}.pco"
    obj.load_cohort(cohort_path)
    file_path = os.getcwd()
    file_name = "multiple_cohort"
    assert obj.create_merged_gct(file_path) is None
    assert obj.create_merged_gct(file_path, file_name) is None
    os.remove(f"{file_path}/{file_name}.gct")
    os.remove(f"{file_path}/{cohort_name_multiple}.gct")


def test_remove_from_cohort_multiple():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_multiple}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    assert obj.remove_from_cohort(dataset_id_multiple) is None


def test_delete_cohort_multiple():
    Polly.auth(token)
    obj = cohort.Cohort()
    cohort_path = f"{os.getcwd()}/{cohort_name_multiple}.pco"
    obj.load_cohort(cohort_path)
    assert obj._cohort_details is not None
    obj.delete_cohort()
    assert obj._cohort_details is None
