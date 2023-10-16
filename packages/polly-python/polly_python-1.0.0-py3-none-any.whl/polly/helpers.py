import os
import re
import json
import logging
import requests
import urllib.request
from cloudpathlib import S3Client
from botocore.exceptions import ClientError
from cmapPy.pandasGEXpress.parse_gct import parse
from os import environ
from polly.errors import (
    BadRequestError,
    error_handler,
    InvalidParameterException,
    MissingKeyException,
    InvalidPathException,
    OperationFailedException,
    paramException,
    AccessDeniedError,
    InvalidRepoException,
    DatatypeNotFoundException,
    RepositoryNotFoundException,
)
from polly.constants import COHORT_CONSTANTS_URL
import contextlib
import joblib
import urllib
import pandas as pd
import polly.http_response_codes as http_codes
from polly.tracking import Track
import polly.constants as const


def get_platform_value_from_env(
    variable: str, default_val: str, passed_val: str
) -> str:
    """
    Get variable value of passed variable
    from os env variables
    """
    if passed_val:
        default_val = passed_val
    elif environ.get(variable, None) is not None:
        POLLY_TYPE = os.getenv(variable)
        env_val = re.search("https://(.+?).elucidata.io", POLLY_TYPE)
        default_val = env_val.group(1)
    return default_val


def make_path(prefix: any, postfix: any) -> str:
    """
    Function to make and return a valid path
    """
    if not prefix:
        raise InvalidParameterException("prefix")
    if not postfix:
        raise InvalidParameterException("postfix")
    return os.path.normpath(f"{prefix}/{postfix}")


def debug_print(self, val: str):
    """Helper function to show prints in test and dev environment

    Args:
        self (polly_session_object): polly_session
        val (str): value to be printed
    """
    if self.session.env != const.PROD_ENV_NAME:
        print(val)


@Track.track_decorator
def debug_logger(self, properties: dict):
    """Track an event but calling the debug logger with properties
    that needs to be tracked
    For Example :-
    If I need to track the Crash of an API and properties related to it
    like which API is crashing, for which page size it crashed and other
    relevant details

    Args:
        properties (dict): Properties of the event which is tracked
    """
    return properties


def get_sts_creds(sts_dict: dict) -> dict:
    """
    Function to check and return temporary sts creds
    """
    if sts_dict and isinstance(sts_dict, dict):
        if "data" in sts_dict:
            data = sts_dict.get("data")
            if "attributes" in data[0]:
                attributes = data[0].get("attributes")
                if "credentials" in attributes:
                    return attributes.get("credentials")
                else:
                    raise MissingKeyException("credentials")
            else:
                raise MissingKeyException("attributes")
        else:
            raise MissingKeyException("data")
    else:
        raise InvalidParameterException("sts_dict")


def merge_dataframes_from_list(df_list: list) -> pd.DataFrame:
    """Takes a list of dfs as argument
    Returns:
        pd.DataFrame: Merge all of them into 1 DF
    """
    if df_list:
        res_df = pd.concat(df_list, axis=0, ignore_index=True)
    else:
        res_df = pd.DataFrame()
    return res_df


def merge_dicts_from_list(dict_list: list) -> dict:
    """Takes a list of dicts as argument
    Returns:
        dict: Merge all of them into 1 dict
    """
    res_dict = {}
    for dict in dict_list:
        res_dict.update(dict)
    return res_dict


def display_df_from_list(val_list: list, column_name_in_df: str):
    """Display dataframe from a flat list and put column name of
    Dataframe that is passed in arguments
    Example :-
    lst = ["abc", "def", "ghi"]
    This lst needs to be converted to dataframe.
    column_name is passed as parameter
    Args:
        val_list (list): list of values to put in dataframe
        column_name_in_df (str): column name for the dataframe
    """
    val_df = pd.DataFrame(val_list, columns=[column_name_in_df])

    with pd.option_context(
        "display.max_rows", 800, "display.max_columns", 800, "display.width", 1200
    ):
        print(val_df)


def upload_to_S3(cloud_path: str, local_path: str, credentials: dict) -> None:
    """
    Function to upload file/folder to S3 cloud path
    """
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]
    client = S3Client(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
        extra_args={"ContentType": "text/html"},
    )
    # use these extras for all CloudPaths
    client.set_as_default_client()
    source_path = client.CloudPath(cloud_path)
    if not source_path.exists():
        source_path.mkdir()
    try:
        source_path.upload_from(local_path, force_overwrite_to_cloud=True)
    except ClientError as e:
        raise OperationFailedException(e)


def download_from_S3(
    cloud_path: str, workspace_path: str, credentials: dict, destination_path: str
) -> None:
    """
    Function to download file/folder from workspaces
    """
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]
    client = S3Client(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
    )
    source_path = client.CloudPath(cloud_path)
    if not source_path.exists():
        raise InvalidPathException
    isFile = source_path.is_file()
    if isFile:
        try:
            source_path.copy(destination_path, force_overwrite_to_cloud=True)
        except ClientError as e:
            raise OperationFailedException(e)
    else:
        if not cloud_path.endswith("/"):
            cloud_path += "/"
        source_path = client.CloudPath(cloud_path)
        if not source_path.is_dir():
            raise InvalidPathException
        try:
            destination_path = f"{make_path(destination_path,workspace_path)}"
            source_path.copytree(destination_path, force_overwrite_to_cloud=True)
        except ClientError as e:
            raise OperationFailedException(e)


def get_workspace_payload(
    cloud_path: str, credentials: dict, source_key: str, source_path: str
):
    """
    Function to return payload for create_copy function
    """
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]
    client = S3Client(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
    )
    source_path = client.CloudPath(cloud_path)
    if not source_path.exists():
        raise InvalidPathException
    isFile = source_path.is_file()
    if isFile:
        payload = {
            "data": [
                {
                    "attributes": {
                        "s3_key": source_key,
                    },
                    "id": "",
                    "type": "file",
                }
            ]
        }
    else:
        if not source_key.endswith("/"):
            source_key += "/"
        payload = {
            "data": [
                {
                    "attributes": {
                        "s3_key": source_key,
                    },
                    "id": "",
                    "type": "folder",
                }
            ]
        }
    return payload


def extract_error_title(error_msg: str) -> str:
    """Extract error title from error message

    Args:
        error_msg (str): Whole Error Message in form of string

    Returns:
        str: Return title of the error message
    """
    error_msg = json.loads(error_msg)
    error = error_msg.get("error")
    if error is None:
        error = error_msg.get("errors")[0]
    if "title" in error:
        title = error.get("title")

    return title


def file_conversion(
    self, repo_info: str, dataset_id: str, format: str, header_mapping: dict
) -> None:
    """
    Function that converts file to mentioned format
    """
    if not (repo_info and isinstance(repo_info, str)):
        raise InvalidParameterException("repo_name/repo_id")
    if not (dataset_id and isinstance(dataset_id, str)):
        raise InvalidParameterException("dataset_id")
    if not (format and isinstance(format, str)):
        raise InvalidParameterException("format")
    if not isinstance(header_mapping, dict):
        raise InvalidParameterException("header_mapping")
    download_dict = self.download_data(repo_info, dataset_id)
    url = download_dict.get("data", {}).get("attributes", {}).get("download_url")
    if not url:
        raise MissingKeyException("dataset url")
    file_name = f"{dataset_id}.gct"
    try:
        urllib.request.urlretrieve(url, file_name)
        data = parse(file_name)
        os.remove(file_name)
        row_metadata = data.row_metadata_df
        if header_mapping:
            row_metadata = row_metadata.rename(header_mapping, axis=1)
        row_metadata.to_csv(f"{dataset_id}.{format}", sep="\t")
    except Exception as e:
        raise OperationFailedException(e)


def get_data_type(self, url: str, payload: dict) -> str:
    """
    Function to return the data-type of the required dataset
    """
    if not (url and isinstance(url, str)):
        raise InvalidParameterException("url")
    if not (payload and isinstance(payload, dict)):
        raise InvalidParameterException("payload")
    response = self.session.post(url, data=json.dumps(payload))
    error_handler(response)
    response_data = response.json()
    hits = response_data.get("hits", {}).get("hits")
    if not (hits and isinstance(hits, list)):
        raise paramException(
            title="Param Error",
            detail="No matches found with the given repo details. Please try again.",
        )
    dataset = hits[0]
    data_type = dataset.get("_source", {}).get("data_type")
    if not data_type:
        raise MissingKeyException("data_type")
    return data_type


# used in move data
def get_metadata(self, url: str, payload: dict) -> str:
    """
    Function to return the data-type of the required dataset
    """
    if not (url and isinstance(url, str)):
        raise InvalidParameterException("url")
    if not (payload and isinstance(payload, dict)):
        raise InvalidParameterException("payload")
    response = self.session.post(url, data=json.dumps(payload))
    error_handler(response)
    response_data = response.json()
    hits = response_data.get("hits", {}).get("hits")
    if not (hits and isinstance(hits, list)):
        raise paramException(
            title="Param Error",
            detail="No dataset matches found in the given repo. Please retry with the correct dataset ID.",
        )
    dataset = hits[0]
    return dataset


# used in move dataset
def elastic_query(index_name: str, dataset_id: str) -> dict:
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"_index": index_name}},
                    {"term": {"dataset_id.keyword": dataset_id}},
                ]
            }
        }
    }
    return query


def get_cohort_constants() -> json:
    """
    Returns cohort info from public assests url
    """
    response = requests.get(COHORT_CONSTANTS_URL)
    error_handler(response)
    return json.loads(response.text)


def validate_datatype(datatype: str):
    """
    Function to validate datatype of a dataset
    Returns 1 in case of datatype is Single Cell, 0 otherwise
    """
    if datatype == "Single cell":
        return 1
    return 0


@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""

    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()


def check_empty(x):
    """
    Function to validate if the entry is an empty list or not.
    """
    if type(x) is list:
        return len("".join(x))
    elif type(x) is float or type(x) is int:
        return 1
    else:
        return len(x)


def get_user_details(session, base_url):
    """
    Function to get user details
    """
    me_url = f"{base_url}/users/me"
    details = session.get(me_url)
    error_handler(details)
    user_details = details.json().get("data", {}).get("attributes")
    return user_details


def generate_aws_pool_url(user_pool_region, user_pool_id):
    verify_url = "https://cognito-idp.{}.amazonaws.com/{}".format(
        user_pool_region, user_pool_id
    )
    return verify_url


def get_public_key(keys, kid):
    """
    Getting public key in pem format from Id Token

    Parameters
    ----------
    keys: Dict
        JWT headers keys
    kid: String
        public key identifier

    Returns
    ----------
    pubk_bytes: String (PEM)
        Public key in pem format
    """

    key = keys[kid]
    return key


def aws_key_dict(region, user_pool_id):
    """
    Fetches the AWS JWT validation file (if necessary) and then converts
    this file into a keyed dictionary that can be used to validate a web-token
    we've been passed

    Parameters
    ----------
    aws_user_pool: String
        AWS Cognito user pool ID
    aws_region: String
        AWS Cognito user pool region

    Returns:
    -------
    dict:
        Contains decoded token dict
    """
    filename = "/tmp/" + "aws_{}.json".format(user_pool_id)

    if not os.path.isfile(filename):
        # If we can't find the file already, try to download it.
        aws_data = requests.get(
            ("https://cognito-idp.{}.amazonaws.com/{}".format(region, user_pool_id))
            + "/.well-known/jwks.json"
        )
        aws_jwt = json.loads(aws_data.text)
        with open(filename, "w+") as json_data:
            json_data.write(aws_data.text)
            json_data.close()

    else:
        with open(filename) as json_data:
            aws_jwt = json.load(json_data)
            json_data.close()

    # We want a dictionary keyed by the kid, not a list.
    result = {}
    for item in aws_jwt["keys"]:
        result[item["kid"]] = item

    return result


def workspaces_permission_check(self, workspace_id) -> bool:
    """
    Function to check access of a user for a given workspace id.
    """
    permission_url = f"{self.base_url}/workspaces/{workspace_id}/permissions"
    response = self.session.get(permission_url, params={"include": "user"})
    error_handler(response)
    user_details = get_user_details(self.session, self.base_url)
    user_id = user_details.get("user_id")
    if "data" in response.json():
        json_data = response.json().get("data")
    else:
        raise BadRequestError(detail="Incorrect response format")
    for user in json_data:
        if "attributes" in user:
            attributes = user.get("attributes")
        else:
            raise BadRequestError(detail="Incorrect response format")
        if user_id == attributes["user_id"] and attributes["project_id"] == int(
            workspace_id
        ):
            if attributes["permission"] != "read":
                return True
            else:
                raise AccessDeniedError(
                    detail=f"Read-only permission over the "
                    f"workspace-id {workspace_id}"
                )
    return False


def return_entity_type(data_source: str, cohort_info: json) -> str:
    """
    Function to return entity type based on the cohort info present in public assets
    """
    if data_source not in cohort_info:
        raise InvalidRepoException(data_source)
    for repo, dict in cohort_info.items():
        if data_source == repo:
            if dict["file_structure"] == "single":
                entity_type = "dataset"
            elif dict["file_structure"] == "multiple":
                entity_type = "sample"
    return entity_type


def get_files_in_dir(path_to_dir: str) -> list:
    """
    returns the files in a given directory

    Arguments:
        path_to_dir: str

    Returns:
        list of files in dir : list
    """
    directory = os.fsencode(path_to_dir)
    file_names = os.listdir(directory)
    return file_names


def make_repo_id_string(repo_id: int) -> str:
    """If repo id is int, change to string
    Args:
        repo_id (int/str): repo id can be int or str
    Returns:
        str: repo id as string type
    """
    if isinstance(repo_id, int):
        repo_id = str(repo_id)
    return repo_id


def parameter_check_for_repo_id(repo_id):
    """Checking for validity of repo id
    Args:
        repo_id (): Repository Id of omixatlas
    Raises:
        paramException: Error if repo id is empty or is not str or int
    """
    if not repo_id:
        raise paramException(
            title="Param Error",
            detail="repo_id should not be empty",
        )
    elif type(repo_id) is not str and type(repo_id) is not int:
        raise paramException(
            title="Param Error",
            detail="repo_id should be str or int",
        )


def parseInt(sin):
    """
    parsed the value passed as int  as done by js.
    python equivalent of js parseInt
    example:
        parseInt("100n")  = 100
        parseInt("400m")  = 400

    Arguments:
        sin -- value to be parsed as int

    Returns:
        int
    """
    m = re.search(r"^(\d+)[.,]?\d*?", str(sin))
    parsed_int = int(m.groups()[-1]) if m and not callable(sin) else None
    return parsed_int


def replace_original_name_field(
    dataset_source_info: dict,
    schema_dict_val: dict,
    dataset_source: str,
    data_type: str,
) -> dict:
    """
    Function to replace original name field for dataset metadata
    Arguments:
    dataset_source_info: dataset metadata to be updated
    schema_dict_val: schema info for the datasets
    repo_name: repository name
    data_type: data_type of the dataset that is required
    Checks for the following cases:
    Case 1: The schema for the particular dataset has source as "all" and datatype as "all"
    Case 2: The schema for the particular dataset has source as "all" and datatype as multiple datatypes
    Case 3: The schema for the particular dataset has source as multiple repositories and datatype as "all"
    Case 4: The schema for the particular dataset has source as multiple repositories and datatype as multiple datatypes
    Currently only Case 1 is valid, but in future the other cases might arrive, hence incorporated the checks accordingly.
    """
    if "all" in schema_dict_val:
        source_dict = schema_dict_val.get("all")
        if "all" in source_dict:
            schema_info = source_dict.get("all")
        elif data_type in source_dict:
            schema_info = source_dict.get(data_type)
        else:
            raise DatatypeNotFoundException(data_type)
    elif dataset_source in schema_dict_val:
        source_dict = schema_dict_val.get(dataset_source)
        if "all" in source_dict:
            schema_info = source_dict.get("all")
        elif data_type in source_dict:
            schema_info = source_dict.get(data_type)
        else:
            raise DatatypeNotFoundException(data_type)
    else:
        raise RepositoryNotFoundException(dataset_source)
    replaced_metadata = {}
    source_keys = dataset_source_info.keys()
    for key in source_keys:
        if key in schema_info:
            original_name = schema_info.get(key).get("original_name")
            replaced_metadata[original_name] = dataset_source_info.get(key)
        else:
            replaced_metadata[key] = dataset_source_info.get(key)
    return replaced_metadata


def upload_html_file(
    session, workspace_id: int, workspace_path: str, local_report_path: str
):
    """
    Function to upload an html file to a workspace.
    """
    upload_url = f"https://v2.api.{session.env}.elucidata.io/workspaces/{workspace_id}/upload_url"
    params = {"file_path": workspace_path, "content_type": "text/html"}
    # get request to get the signed url for s3
    response = session.get(upload_url, params=params)
    error_handler(response)
    attributes = response.json().get("data").get("attributes")
    try:
        with open(local_report_path, "rb") as file_to_upload:
            # uploading the local file to the signed url
            files = {"file": (local_report_path, file_to_upload)}
            upload_response = requests.post(
                attributes["url"], data=attributes["fields"], files=files
            )
            error_handler(upload_response)
            if upload_response.status_code == http_codes.CREATED:
                logging.basicConfig(level=logging.INFO)
                logging.info(
                    f"File uploaded successfully to workspace-id = {workspace_id} at path = {workspace_path}!"
                )
    except Exception as e:
        raise e


def get_folder_list_from_list_of_filepaths(filenames_fullpath_list: list) -> list:
    """
    gives back only the folders from a list of filepaths provided.
    for example: given a list ["transcriptomics.gct","folder1/transcriptomics.gct"]
    returned value: [".","folder1"]

    Arguments:
        filenames_fullpath_list -- list of filenames with full paths
    """
    list_folder_names = []
    for full_file_path in filenames_fullpath_list:
        folder_name = os.path.normpath(os.path.dirname(full_file_path))
        list_folder_names.append(folder_name)
    return list(set(list_folder_names))


def make_query_for_discover_api(page_size, dataset_id):
    query = {
        "query": {
            "term": {
                # Count entries for the following key-value pairs
                "src_dataset_id.keyword": dataset_id
            }
        },
        # Fetch X many rows at a time (you will still get the full output, which may be greater than 10K)
        # Setting this value to be greater than 10k will result in an error
        "size": page_size,
    }
    return query


def read_json(path: str) -> json:
    """
    Function to read json content from a file.
    """
    with open(path) as filepath:
        return json.load(filepath)


def remove_prefix(text: str, prefix: str) -> str:
    """
    Function to remove prefix from text.
    """
    if text.startswith(prefix):
        slice_obj = slice(len(prefix), len(text))
        return text[slice_obj]
    return text


def find_between(s, first, last) -> str:
    """Function to find the elements between first and last boundary elements
    Using this function, a substring can be extract which is between two elements
    first and last
    Reference
    https://stackoverflow.com/questions/3368969/find-string-between-two-substrings

    Args:
        s (str): main string from
        first (str): first boundary elements
        last (str): last boundary elements

    Returns:
        str: substring b/w boundary elements
    """
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        # write proper error message here
        raise Exception("Error extracting substring. Please contact admin")
