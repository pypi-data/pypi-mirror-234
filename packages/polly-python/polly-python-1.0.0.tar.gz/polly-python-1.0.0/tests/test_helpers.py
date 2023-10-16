import pytest
import polly.helpers as helpers
from polly.constants import COMPUTE_ENV_VARIABLE
from polly.errors import InvalidParameterException


def test_get_platform_value_from_env():
    default_env = "polly"
    env = "testpolly"
    val = helpers.get_platform_value_from_env(COMPUTE_ENV_VARIABLE, default_env, env)
    assert isinstance(val, str)
    assert val == "testpolly"


def test_make_path():
    valid_prefix = "prefix"
    invalid_prefix = ""
    valid_postfix = "postfix"
    invalid_postfix = ""
    assert helpers.make_path(valid_prefix, valid_postfix) is not None
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        helpers.make_path(valid_prefix, invalid_postfix)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        helpers.make_path(invalid_prefix, valid_postfix)


def test_elastic_query():
    index_name = "index_name"
    dataset_id = "dataset_id"
    assert helpers.elastic_query(index_name, dataset_id) is not None


def test_get_cohort_constants():
    assert helpers.get_cohort_constants() is not None


def test_check_empty():
    test_argument_1 = ["value"]
    test_argument_2 = "value"
    test_argument_3 = 10
    assert helpers.check_empty(test_argument_1) is not None
    assert helpers.check_empty(test_argument_2) is not None
    assert helpers.check_empty(test_argument_3) is not None


def test_validate_datatype_single_cell():
    datatype = "Single cell"

    res = helpers.validate_datatype(datatype)
    assert res == 1


def test_validate_datatype_rna_seq():
    datatype = "Rna seq"

    res = helpers.validate_datatype(datatype)
    assert res == 0
