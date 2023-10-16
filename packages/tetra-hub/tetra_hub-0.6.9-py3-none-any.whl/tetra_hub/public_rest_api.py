from __future__ import annotations

import configparser
import datetime
import json
import mimetypes
import os
import posixpath
import shutil
import tempfile
import threading
from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import quote, urljoin
from zipfile import ZipFile

import numpy as np
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

from tetra_hub.util.session import create_session

from . import api_status_codes
from . import public_api_pb2 as api_pb

UNKNOWN_ERROR = "Unknown error."
API_VERSION = "v1"

# Used for error message feedback
CASUAL_CLASSNAMES = {
    api_pb.ProfileJob: "job",
    api_pb.Model: "model",
    api_pb.User: "user",
}

TETRA_CLIENT_ENV = "TETRA_CLIENT_INI"
DEFAULT_CONFIG_PATH = "~/.tetra/client.ini"

_InputSpec = Tuple[Tuple[int, ...], str]
_InputSpecsList = List[Tuple[str, _InputSpec]]
InputSpecs = Dict[str, Union[Tuple[int, ...], _InputSpec]]
DatasetEntries = Dict[str, List[np.ndarray]]


def get_config_path(expanduser=True):
    path = os.environ.get(TETRA_CLIENT_ENV, DEFAULT_CONFIG_PATH)
    if expanduser:
        path = os.path.expanduser(path)
    return path


@dataclass
class ClientConfig:
    """
    Configuration information, such as your API token, for use with
    :py:class:`.Client`.

    Parameters
    ----------
    api_url
        URL of the API backend endpoint.
    web_url
        URL of the web interface.
    api_token
        API token. Available through the web interface under the "Account" page.
    verbose
        Verbosity of terminal output (eg. whether to print status bars for uploads & downloads)
    """

    api_url: str
    web_url: str
    api_token: str
    verbose: bool


class APIException(Exception):
    """
    Exception for the python REST API.

    Parameters
    ----------
    message : str
        Message of the failure. If None, sets it automatically based on
        `status_code`.
    status_code : int
        API status code (a superset of HTTP status codes).
    """

    def __init__(self, message=None, status_code=None):
        if message is None:
            if status_code is not None:
                # Some common error codes have custom messages
                if status_code == api_status_codes.HTTP_401_UNAUTHORIZED:
                    message = "API authentication failure; please check your API token."
                elif status_code == api_status_codes.HTTP_429_TOO_MANY_REQUESTS:
                    message = "Too Many Requests: please slow down and try again soon."
                elif status_code == api_status_codes.API_CONFIGURATION_MISSING_FIELDS:
                    config_path = get_config_path(expanduser=False)
                    message = f"Required fields are missing from your {config_path}."
                elif status_code == api_status_codes.HTTP_413_REQUEST_ENTITY_TOO_LARGE:
                    message = "The uploaded asset is too large. Please contact us for workarounds."
                else:
                    message = f"API request returned status code {status_code}."
            else:
                message = UNKNOWN_ERROR

        super().__init__(message)
        self.status_code = status_code


def _response_as_protobuf(
    response: requests.Response, protobuf_class: Any, obj_id: Optional[int] = None
) -> Any:
    if (
        api_status_codes.is_success(response.status_code)
        and response.headers.get("Content-Type") == "application/x-protobuf"
    ):
        pb = protobuf_class()
        pb.ParseFromString(response.content)
        return pb
    elif (
        response.status_code == api_status_codes.HTTP_404_NOT_FOUND
        and obj_id is not None
    ):
        prefix = ""
        class_name = CASUAL_CLASSNAMES.get(protobuf_class)
        if class_name is not None:
            prefix = class_name.capitalize() + " "

        raise APIException(
            f"{prefix}ID {obj_id} could not be found. It may not exist or you may not have permission to view it.",
            status_code=response.status_code,
        )
    elif response.status_code == api_status_codes.HTTP_403_FORBIDDEN:
        raise APIException(
            response.content,
            status_code=response.status_code,
        )
    else:
        raise APIException(status_code=response.status_code)


def _prepare_offset_limit_query_list(offset: int, limit: Optional[int]) -> List[str]:
    extras = []
    if offset > 0:
        extras.append(f"offset={offset}")
    if limit is not None:
        extras.append(f"limit={limit}")
    return extras


def _prepare_offset_limit_query(offset: int, limit: Optional[int]) -> str:
    extras = _prepare_offset_limit_query_list(offset, limit)
    if extras:
        return "?" + "&".join(extras)
    else:
        return ""


def _load_default_api_config(verbose=False) -> ClientConfig:
    """
    Load a default ClientConfig from default locations.

    Parameters
    ----------
    verbose : bool
        Print where config file is loaded from.

    Returns
    -------
    config : ClientConfig
        API authentication configuration.
    """
    # Load from default config path
    config = configparser.ConfigParser()
    # Client config should be in ~/.tetra/client.ini
    tilde_config_path = get_config_path(expanduser=False)
    config_path = os.path.expanduser(tilde_config_path)
    if verbose:
        print(f"Loading Client config from {tilde_config_path} ...")
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"{tilde_config_path} not found. Please request access to Tetra Hub by contacting support@tetra.ai. If you have access, please go to the Account page to find instructions of how to install your API key."
        )
    config.read([config_path])
    try:
        client_config = config["api"]

        api_config = ClientConfig(
            api_url=client_config["api_url"],
            web_url=client_config["web_url"],
            api_token=client_config["api_token"],
            verbose=utils.str2bool(client_config["verbose"])
            if "verbose" in client_config
            else True,
        )
    except KeyError:
        raise APIException(
            status_code=api_status_codes.API_CONFIGURATION_MISSING_FIELDS
        )
    return api_config


def _auth_header(
    config: ClientConfig, content_type: str = "application/x-protobuf"
) -> dict:
    header = {
        "Authorization": f"token {config.api_token}",
        "Content-Type": content_type,
    }
    return header


def _api_url(config: ClientConfig, *rel_paths) -> str:
    return urljoin(config.api_url, posixpath.join("api", API_VERSION, *rel_paths, ""))


def _get_token(api_url, email, password):
    url = urljoin(
        api_url, posixpath.join("api", API_VERSION, "users", "auth", "login", "")
    )
    data = {"email": email, "password": password}
    header = {"Content-Type": "application/json"}
    response = create_session().post(url, headers=header, data=json.dumps(data))
    if api_status_codes.is_success(response.status_code):
        return json.loads(response.content)["key"]
    elif response.status_code == 400:
        raise ValueError("Failed to log in: Wrong Username / Password")
    else:
        raise APIException(status_code=response.status_code)


_STR_TO_TETRA_TYPE: Dict[str, api_pb.TensorDtype.ValueType] = {
    "float32": api_pb.TensorDtype.TENSOR_DTYPE_FLOAT32,
    "int32": api_pb.TensorDtype.TENSOR_DTYPE_INT32,
    "int8": api_pb.TensorDtype.TENSOR_DTYPE_INT8,
    "uint8": api_pb.TensorDtype.TENSOR_DTYPE_UINT8,
}
_TETRA_TYPE_TO_STR: Dict[api_pb.TensorDtype.ValueType, str] = {
    v: k for k, v in _STR_TO_TETRA_TYPE.items()
}


def _str2bool(s: str) -> bool:
    if s.lower() in ("yes", "true", "t", "1"):
        return True
    if s.lower() in ("no", "false", "f", "0"):
        return False
    raise ValueError(f"Unrecognized boolean string value {s}")


def _get_type_str_from_value(type: api_pb.TensorDtype.ValueType) -> str:
    dtype = _TETRA_TYPE_TO_STR.get(type, None)
    if dtype is None:
        raise ValueError("Unknown tensor dtype")
    return dtype


def _get_type_vale_from_str(dtype: str) -> api_pb.TensorDtype.ValueType:
    type = _STR_TO_TETRA_TYPE.get(dtype, None)
    if type is None:
        raise ValueError(
            f"Unsupported tensor dtype={dtype}. Supported dtypes: {list(_STR_TO_TETRA_TYPE.keys())}"
        )
    return type


def _create_named_tensor(
    name: str, shape: Tuple[int, ...], type: str
) -> api_pb.NamedTensorType:
    tensor_type_list = []
    for i in shape:
        tensor_type_list.append(i)
    tensor_type_pb = api_pb.TensorType(
        shape=tensor_type_list, dtype=_get_type_vale_from_str(type)
    )
    return api_pb.NamedTensorType(name=name, tensor_type=tensor_type_pb)


def _input_shapes_to_tensor_type_list_pb(
    input_shapes: InputSpecs,
) -> api_pb.NamedTensorTypeList:
    tensor_type_pb_list = []

    if input_shapes is not None:
        for name, spec in input_shapes.items():
            if isinstance(spec[0], tuple):
                shape = spec[0]
                dtype = spec[1]
            else:
                shape = spec  # type: ignore
                dtype = "float32"

            assert isinstance(dtype, str)
            assert isinstance(shape, tuple)
            named_tensor_type_pb = _create_named_tensor(name, shape, dtype)
            tensor_type_pb_list.append(named_tensor_type_pb)

    return api_pb.NamedTensorTypeList(types=tensor_type_pb_list)


def _tensor_type_list_pb_to_list_shapes(
    tensor_type_list_pb: api_pb.NamedTensorTypeList,
) -> _InputSpecsList:
    shapes_list = []

    for t in tensor_type_list_pb.types:
        type = _get_type_str_from_value(t.tensor_type.dtype)
        shape = tuple([int(d) for d in t.tensor_type.shape])
        shapes_list.append((t.name, (shape, type)))

    return shapes_list


_get_unique_path_lock = threading.Lock()


def _get_unique_path(dst_path: str) -> Tuple[str, str]:
    name, ext = os.path.splitext(dst_path)
    if ext == ".zip":
        name, sub_ext = os.path.splitext(name)
        ext = sub_ext + ext

    _get_unique_path_lock.acquire()
    if os.path.exists(dst_path):
        now = str(datetime.datetime.now().time()).replace(":", ".")
        dst_path = f"{name}_{now}{ext}"

    # Write empty file (to be overwritten later), for thread safety.
    open(dst_path, "a").close()

    _get_unique_path_lock.release()

    name = os.path.basename(dst_path)

    return dst_path, name


def _convert_inputs_to_tensor_type_list_pb(
    inputs: DatasetEntries,
) -> api_pb.NamedTensorTypeList:
    tensor_type_pb_list = []
    for name, tensor in inputs.items():
        named_tensor_type_pb = _create_named_tensor(
            name, tensor[0].shape, tensor[0].dtype.name
        )
        tensor_type_pb_list.append(named_tensor_type_pb)
    return api_pb.NamedTensorTypeList(types=tensor_type_pb_list)


def _input_shapes_dict_to_list(input_shapes: InputSpecs) -> _InputSpecsList:
    return _tensor_type_list_pb_to_list_shapes(
        _input_shapes_to_tensor_type_list_pb(input_shapes)
    )


def _do_input_shapes_match(
    input_shapes: InputSpecs,
    tensor_type_list: api_pb.NamedTensorTypeList,
):
    inputs_tensor_type_list = _tensor_type_list_pb_to_list_shapes(tensor_type_list)
    inputs_shapes_tensor_type_list = _input_shapes_dict_to_list(input_shapes)

    input_names_match = [False] * len(inputs_tensor_type_list)
    for i, (input_name, input_tensor_spec) in enumerate(inputs_tensor_type_list):
        for _, (input_shape_name, input_spec) in enumerate(
            inputs_shapes_tensor_type_list
        ):
            if input_name == input_shape_name:
                input_names_match[i] = True
                if input_tensor_spec != input_spec:
                    return False
    return all(input_names_match)


def _download_file(
    url: str,
    filename: str,
    dst_path: str,
    verbose: bool,
    extract_if_zipped: bool = False,
) -> str:
    dst_path = os.path.expanduser(dst_path)  # Expand ~ to user home in path.

    # Unzip file only if extract_if_zipped is set and uploaded file is zipped.
    file_to_be_extracted = extract_if_zipped and filename.endswith(".zip")

    # If no filename is provided, use the filename given to us by the parent
    if os.path.isdir(dst_path):
        dst_path = os.path.join(dst_path, filename)

        # Append numerical suffix to the filename if the dst file already exists.
        dst_path, filename = _get_unique_path(dst_path)

        # Remove .zip extension from destination path
        if file_to_be_extracted:
            dst_path = os.path.splitext(dst_path)[0]
    elif file_to_be_extracted:
        raise ValueError(
            "Model cannot be extracted to a file. Please provide a directory path."
        )

    # Verify dst parent dir exists. The same error thrown by open() called
    # below would include the model name, which is confusing.
    parent_dir = os.path.dirname(dst_path)
    if parent_dir and not os.path.exists(parent_dir):
        raise ValueError(f"Download directory '{parent_dir}' does not exist.")

    response = create_session().get(url, stream=True)
    if api_status_codes.is_success(response.status_code):
        file_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        if verbose:
            tqdm_context = tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=block_size,
                colour="magenta",
                desc=filename,
            )
        else:
            tqdm_context = nullcontext()

        with tqdm_context as progress_bar:
            # Download to a temporary directory first, so if the download
            # fails or is cancelled midway, the user isn't left with a
            # useless partial artifact on disk.
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_dst_path = os.path.join(tmpdir, os.path.basename(dst_path))
                with open(tmp_dst_path, "wb") as fd:
                    for data in response.iter_content(block_size):
                        written_data = fd.write(data)
                        if progress_bar:
                            progress_bar.update(written_data)

                if file_to_be_extracted:
                    with ZipFile(tmp_dst_path, "r") as zippedModel:
                        zippedModel.extractall(dst_path)
                    os.remove(tmp_dst_path)
                else:
                    # Cannot use os.rename, whose doc string states: "On
                    # Windows, if dst exists a FileExistsError is always
                    # raised." `dst_path` is always created by
                    # `_get_unique_path`
                    # `os.replace` gives "The system cannot move the file to a
                    # different disk drive"
                    shutil.move(tmp_dst_path, dst_path)
    else:
        raise APIException(status_code=response.status_code)

    return dst_path


def _quote_query_parameters(query_param: str) -> str:
    return quote(query_param.encode("utf-8"))


def _guess_file_http_content_type(path: str) -> str:
    # `.log` is not supported by mimetypes on linux.
    if path.endswith(".log"):
        return "text/plain"

    file_type, _ = mimetypes.guess_type(path, strict=True)
    return file_type or "application/octet-stream"


# These helper functions are placed in a utils namespace
# so as not to confuse with core API functions
utils = SimpleNamespace(
    response_as_protobuf=_response_as_protobuf,
    prepare_offset_limit_query=_prepare_offset_limit_query,
    prepare_offset_limit_query_list=_prepare_offset_limit_query_list,
    load_default_api_config=_load_default_api_config,
    auth_header=_auth_header,
    api_url=_api_url,
    input_shapes_to_tensor_type_list_pb=_input_shapes_to_tensor_type_list_pb,
    tensor_type_list_pb_to_list_shapes=_tensor_type_list_pb_to_list_shapes,
    get_unique_path=_get_unique_path,
    download_file=_download_file,
    convert_inputs_to_tensor_type_list_pb=_convert_inputs_to_tensor_type_list_pb,
    do_input_shapes_match=_do_input_shapes_match,
    input_shapes_dict_to_list=_input_shapes_dict_to_list,
    quote_query_parameters=_quote_query_parameters,
    get_type_str_from_value=_get_type_str_from_value,
    get_type_vale_from_str=_get_type_vale_from_str,
    guess_file_http_content_type=_guess_file_http_content_type,
    str2bool=_str2bool,
)


def get_auth_user(config: ClientConfig) -> api_pb.User:
    """
    Get authenticated user information.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    user_pb : User
        Get authenticated user information.
    """
    url = utils.api_url(config, "users", "auth", "user")
    header = utils.auth_header(config)
    response = create_session().get(url, headers=header)
    if api_status_codes.is_success(response.status_code):
        return utils.response_as_protobuf(response, api_pb.User)
    else:
        raise APIException(status_code=response.status_code)


def get_user(config: ClientConfig, user_id: int) -> api_pb.User:
    """
    Get user information.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    user_id : int
        User ID.

    Returns
    -------
    user_pb : User
       User information as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "users", str(user_id))
    header = utils.auth_header(config)
    response = create_session().get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.User, obj_id=user_id)


def get_user_list(
    config: ClientConfig, offset: int = 0, limit: int | None = None
) -> api_pb.UserList:
    """
    Get user information.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    offset : int
        Offset the query.
    limit : int
        Limit query response size.

    Returns
    -------
    user_list_pb : UserList
       User list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "users")
    url += utils.prepare_offset_limit_query(offset, limit)
    header = utils.auth_header(config)
    response = create_session().get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.UserList)


def get_device_list(
    config: ClientConfig,
    name: str = "",
    os: str = "",
    attributes: List[str] = [],
    select: bool = False,
) -> api_pb.DeviceList:
    """
    Get list of active devices.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    name : str
        Only devices with this exact name will be returned.
    os : str
        Only devices with an OS version that is compatible with this os are returned
    attributes : List[str]
        Only devices that have all requested properties are returned.
    select: bool
        whether to return a list or a single device

    Returns
    -------
    device_list_pb : DeviceList
       Device list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "devices")
    name = utils.quote_query_parameters(name)
    os = utils.quote_query_parameters(os)
    select = utils.quote_query_parameters(str(select))
    url += f"?name={name}&os={os}&select={select}"
    for attr in attributes:
        attr = utils.quote_query_parameters(attr)
        url += f"&attributes={attr}"
    header = utils.auth_header(config)
    response = create_session().get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.DeviceList)


def create_compilation_job(
    config: ClientConfig, compilation_job_pb: api_pb.CompilationJob
) -> api_pb.CreateUpdateResponse:
    """
    Create new profile job.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_pb : CompilationJob
        Protobuf object with new compilation job.

    Returns
    -------
    response_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse. If successful, ``id`` will be nonzero.
        If failure, ``id`` will be zero and ``status`` will contain an error.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "jobs")
    header = utils.auth_header(config)
    job_pb = api_pb.Job(compilation_job=compilation_job_pb)
    response = requests.post(
        url,
        data=job_pb.SerializeToString(),
        headers=header,
    )
    response_pb: api_pb.CreateUpdateResponse = utils.response_as_protobuf(
        response, api_pb.CreateUpdateResponse
    )
    if len(response_pb.id) == 0:
        raise ValueError("Failed to create compilation job: " + response_pb.status)
    return response_pb


def create_profile_job(
    config: ClientConfig, profile_job_pb: api_pb.ProfileJob
) -> api_pb.CreateUpdateResponse:
    """
    Create new profile job.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_pb : ProfileJob
        Protobuf object with new profile job.

    Returns
    -------
    response_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse. If successful, ``id`` will be nonzero.
        If failure, ``id`` will be zero and ``status`` will contain an error.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "jobs")
    header = utils.auth_header(config)
    job_pb = api_pb.Job(profile_job=profile_job_pb)
    response = create_session().post(
        url,
        data=job_pb.SerializeToString(),
        headers=header,
    )
    response_pb: api_pb.CreateUpdateResponse = utils.response_as_protobuf(
        response, api_pb.CreateUpdateResponse
    )
    if len(response_pb.id) == 0:
        raise ValueError("Failed to create profile job: " + response_pb.status)
    return response_pb


def create_validation_job(
    config: ClientConfig, validation_job_pb: api_pb.ValidationJob
) -> api_pb.CreateUpdateResponse:
    """
    Create new validation job.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_pb : ValidationJob
        Protobuf object containing properties for the new validation job

    Returns
    -------
    response_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse. If successful, ``id`` will be nonzero.
        If failure, ``id`` will be zero and ``status`` will contain an error.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "jobs")
    header = utils.auth_header(config)
    job_pb = api_pb.Job(validation_job=validation_job_pb)
    response = create_session().post(
        url,
        data=job_pb.SerializeToString(),
        headers=header,
    )
    response_pb: api_pb.CreateUpdateResponse = utils.response_as_protobuf(
        response, api_pb.CreateUpdateResponse
    )
    if len(response_pb.id) == 0:
        raise ValueError("Failed to create validation job: " + response_pb.status)
    return response_pb


def get_job(config: ClientConfig, job_id: str) -> api_pb.Job:
    """
    Get job information.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_id : str
        Job ID.

    Returns
    -------
    job_pb : ProfileJob
        Profile job as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "jobs", job_id)
    header = utils.auth_header(config)
    response = create_session().get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.Job, obj_id=job_id)


def get_job_list(
    config: ClientConfig,
    offset: int = 0,
    limit: int | None = None,
    states: List["api_pb.JobState.ValueType"] = [],
    job_type: "api_pb.JobType.ValueType" = api_pb.JobType.JOB_TYPE_UNSPECIFIED,
    creator: str | None = None,
) -> api_pb.JobList:
    """
    Get list of jobs visible to the authenticated user.

    Parameters
    ----------
    config :
        API authentication configuration.
    offset : int
        Offset the query.
    limit : int
        Limit query response size.
    states :
        Filter by list of states.
    job_type :
        Filter by job type. JOB_TYPE_UNSPECIFIED will return all jobs.
    creator:
        Filter by job creator. If unspecified, will return all jobs created by anyone in the user's organization.

    Returns
    -------
    list_pb : JobList
        List of jobs as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "jobs")

    # TODO: better API for joining optional query strings.
    query_components = []
    query_components += utils.prepare_offset_limit_query_list(offset, limit)
    if creator:
        query_components.append(f"creator={creator}")
    if states:
        states_str = ",".join([str(x) for x in states])
        states_query = f"state={states_str}"
        query_components.append(states_query)
    if job_type != api_pb.JobType.JOB_TYPE_UNSPECIFIED:
        job_type_query = f"type={job_type}"
        query_components.append(job_type_query)
    if query_components:
        url += "?" + "&".join(query_components)

    header = utils.auth_header(config)
    response = create_session().get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.JobList)


def get_job_results(config: ClientConfig, job_id: str) -> api_pb.JobResult:
    """
    Get job results, if available.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_id : str
        Job ID as integer.

    Results
    -------
    res_pb : ProfileJobResult
        Result is returned as a protobuf object. Or None if results are not available.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)
    url = utils.api_url(config, "jobs", job_id, "result")
    response = create_session().get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.JobResult, obj_id=job_id)


def get_profile_job_vizgraph(config: ClientConfig, job_id: str) -> api_pb.VizGraph:
    """
    Get profile job vizgraph, if available.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_id : str
        Profile job ID.

    Results
    -------
    vizgraph_pb : VizGraph
        Visualization graph representing the job.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)
    url = utils.api_url(config, "jobs", job_id, "profile", "vizgraph")
    response = create_session().get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.VizGraph, obj_id=job_id)


# Workaround for mypy having trouble with globals https://github.com/python/mypy/issues/5732
last: int


def _upload_asset(
    upload_url: str,
    path: str | Path,
    file_field_name: str,
    fields: Dict[str, Any] = {},
    verbose: bool = True,
    progress_bar_description: Optional[str] = None,
) -> None:
    """
    Helper upload function for models, datasets, etc.
    """
    path = os.path.expanduser(path)  # Expand home directory prefix.

    try:
        total_size = os.path.getsize(path)
    except FileNotFoundError:
        raise

    global last
    last = 0
    if verbose:
        tqdm_context = tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            colour="magenta",
            desc=progress_bar_description,
        )

        def update_progress(monitor):
            global last
            # Your callback function
            tqdm_context.update(monitor.bytes_read - last)
            last = monitor.bytes_read

    else:

        def update_progress(monitor):
            pass

    # We must manually edit the upload URL to follow redirects. The upload fails
    # if we allow python requests to auto-redirect during the multipart upload,
    # because requests will change all redirects to GET requests
    # (https://github.com/psf/requests/issues/1325)
    #
    #
    # Therefore, there are two potential paths here:
    # - the requests library will follow redirect responses until it gets a non-redirect response
    # - immediately get some non-redirect response back
    #
    # In either case, the non-redirect response we recieve doesn't matter; it's thrown away.
    # response.url will be populated with the last URL the requests package tried.
    # This will be the redirected URL if applicable, or the original URL if there was no redirect.
    #
    with open(path, "rb") as asset_file:
        fields[file_field_name] = (
            "model",
            asset_file,
            utils.guess_file_http_content_type(str(path)),
        )
        num_redirects = 0
        while True:
            asset_file.seek(0)
            mpe = MultipartEncoder(fields=fields)
            mpm = MultipartEncoderMonitor(mpe, update_progress)
            headers = {"content-type": mpm.content_type}

            response = create_session().post(
                upload_url, allow_redirects=False, data=mpm, headers=headers
            )
            if (
                response.status_code
                in [
                    requests.codes.moved,
                    requests.codes.found,
                    requests.codes.temporary_redirect,
                    requests.codes.permanent_redirect,
                ]
                and num_redirects < 5
            ):
                num_redirects += 1
                upload_url = response.headers["Location"]
            else:
                break

    if not api_status_codes.is_success(response.status_code):
        raise APIException(f"Failed to upload the file. Detail: {response.reason}")

    update_progress(SimpleNamespace(bytes_read=total_size))


def _create_model(
    config: ClientConfig,
    name: str,
    model_type: "api_pb.ModelType.ValueType",
    verbose: bool | None = None,
) -> api_pb.CreateUpdateResponse:
    """
    Create a model object.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    name : str
        Name of the model. If None, uses basename of path.
    model_type : api_pb.ModelType
        Type of the model.
    verbose : bool | None
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    model_pb = api_pb.Model(name=name, model_type=model_type)
    url = utils.api_url(config, "models")
    response_pb: api_pb.CreateUpdateResponse = utils.response_as_protobuf(
        create_session().post(url, data=model_pb.SerializeToString(), headers=header),
        api_pb.CreateUpdateResponse,
    )
    if len(response_pb.id) == 0:
        raise ValueError("Failed to create model: " + response_pb.status)
    return response_pb


def _get_model_upload_url(
    config: ClientConfig, model_id: str, verbose: bool | None = None
) -> api_pb.FileUploadURL:
    """
    Get the URL with which the user should upload the model file.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    model_id : str
        ID of the model to query.
    verbose : bool | None
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : FileUploadURL
        Returns a FileUploadURL protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    url = utils.api_url(config, f"models/{model_id}/upload_url")
    return utils.response_as_protobuf(
        create_session().get(url, headers=header),
        api_pb.FileUploadURL,
    )


def _confirm_model_upload(
    config: ClientConfig, model_id: str, verbose: bool | None = None
) -> api_pb.CreateUpdateResponse:
    """
    Confirm to hub that the upload for the corresponding model is complete.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    model_id : str
        ID of the model to update.
    verbose : bool
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    model_pb = api_pb.Model(file_upload_complete=True)
    url = utils.api_url(config, f"models/{model_id}")
    response_pb: api_pb.CreateUpdateResponse = utils.response_as_protobuf(
        create_session().patch(url, data=model_pb.SerializeToString(), headers=header),
        api_pb.CreateUpdateResponse,
    )
    if len(response_pb.id) == 0:
        raise ValueError("Failed to confirm model upload: " + response_pb.status)
    return response_pb


def create_and_upload_model(
    config: ClientConfig,
    path: str,
    model_type,
    name: Optional[str] = None,
    verbose: bool | None = None,
) -> api_pb.CreateUpdateResponse:
    """
    Create a model object and upload the corresponding model file.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    path : str or Path
        Local path to the model file.
    name : str
        Name of the model. If None, uses basename of path.
    model_type : api_pb.ModelType
        Type of the model.
    verbose : bool | None
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if not name:
        name = os.path.basename(path)

    verbose = verbose if verbose is not None else config.verbose

    # Create the model object
    cup_create_model = _create_model(config, name, model_type, verbose)
    if not cup_create_model.id or cup_create_model.status:
        return cup_create_model
    model_id = cup_create_model.id

    # Get model upload URL
    model_url = _get_model_upload_url(config, model_id, verbose)

    # Convert proto fields to a python dict.
    fields = {}
    for k, v in model_url.fields.items():
        fields[k] = v

    # Upload the model asset file
    _upload_asset(
        upload_url=model_url.url,
        path=path,
        file_field_name=model_url.file_field_name,
        fields=fields,
        verbose=verbose,
        progress_bar_description="Uploading model",
    )

    # Tell Hub that the model upload is done.
    upload_pb = _confirm_model_upload(config, model_id, verbose)
    cup_create_model.id = upload_pb.id
    return cup_create_model


def _create_dataset(
    config: ClientConfig, name: str, verbose: bool | None = None
) -> api_pb.CreateUpdateResponse:
    """
    Create a dataset object.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    name : str
        Name of the dataset.
    verbose : bool
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    dataset_pb = api_pb.Dataset(name=name)
    url = utils.api_url(config, "datasets")
    response_pb: api_pb.CreateUpdateResponse = utils.response_as_protobuf(
        create_session().post(url, data=dataset_pb.SerializeToString(), headers=header),
        api_pb.CreateUpdateResponse,
    )
    if len(response_pb.id) == 0:
        raise ValueError("Failed to create dataset: " + response_pb.status)
    return response_pb


def _get_dataset_upload_url(
    config: ClientConfig, dataset_id: str, verbose: bool | None = None
) -> api_pb.FileUploadURL:
    """
    Get the URL with which the user should upload the dataset file.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    dataset_id : str
        ID of the dataset to query.
    verbose : bool | None
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : FileUploadURL
        Returns a FileUploadURL protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    url = utils.api_url(config, f"datasets/{dataset_id}/upload_url")
    return utils.response_as_protobuf(
        create_session().get(url, headers=header),
        api_pb.FileUploadURL,
    )


def _confirm_dataset_upload(
    config: ClientConfig, dataset_id: str, verbose: bool | None = None
) -> api_pb.CreateUpdateResponse:
    """
    Confirm to hub that the upload for the corresponding dataset is complete.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    dataset_id : str
        ID of the dataset to query.
    verbose : bool | None
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    dataset_pb = api_pb.Dataset(file_upload_complete=True)
    url = utils.api_url(config, f"datasets/{dataset_id}")
    response_pb: api_pb.CreateUpdateResponse = utils.response_as_protobuf(
        create_session().patch(
            url, data=dataset_pb.SerializeToString(), headers=header
        ),
        api_pb.CreateUpdateResponse,
    )
    if len(response_pb.id) == 0:
        raise ValueError("Failed to confirm dataset upload: " + response_pb.status)
    return response_pb


def create_and_upload_dataset(
    config: ClientConfig,
    path: str | Path,
    name: str,
    verbose: bool | None = None,
) -> api_pb.CreateUpdateResponse:
    """
    Create dataset and upload the corresponding h5 file.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    path : str or Path
        Local path to the model file.
    name : Optional[str]
        Name of the model.
    verbose : bool | None
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    verbose = verbose if verbose is not None else config.verbose

    # Create the dataset object
    cup_create_dataset = _create_dataset(config, name, verbose)
    if not cup_create_dataset.id or cup_create_dataset.status:
        return cup_create_dataset
    dataset_id = cup_create_dataset.id

    # Get dataset upload URL
    dataset_url = _get_dataset_upload_url(config, dataset_id, verbose)

    # Convert proto fields to a python dict.
    fields = {}
    for k, v in dataset_url.fields.items():
        fields[k] = v

    # Upload the dataset asset file
    _upload_asset(
        upload_url=dataset_url.url,
        path=path,
        file_field_name=dataset_url.file_field_name,
        fields=fields,
        verbose=verbose,
        progress_bar_description="Uploading dataset",
    )

    # Tell Hub that the dataset upload is done.
    upload_pb = _confirm_dataset_upload(config, dataset_id, verbose)
    cup_create_dataset.id = upload_pb.id
    return cup_create_dataset


def get_dataset(config: ClientConfig, dataset_id: str) -> api_pb.Dataset:
    """
    Get info about an uploaded dataset.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    dataset_id : str
        Dataset ID.

    Returns
    -------
    dataset_pb : Dataset
        Dataset info as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "datasets", dataset_id)
    header = utils.auth_header(config)
    response = create_session().get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.Dataset, obj_id=dataset_id)


def get_dataset_list(
    config: ClientConfig, offset: int = 0, limit: int | None = None
) -> api_pb.DatasetList:
    """
    Get list of datasets visible to the authenticated user.


    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    offset : int
        Offset the query.
    limit : int | None
        Limit query response size.

    Returns
    -------
    list_pb : DatasetList
        Dataset list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "datasets")
    url += utils.prepare_offset_limit_query(offset, limit)
    header = utils.auth_header(config)
    response = create_session().get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.DatasetList)


def get_model(config: ClientConfig, model_id: str) -> api_pb.Model:
    """
    Get info about an uploaded model.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    model_id : str
        Model ID.

    Returns
    -------
    model_pb : Model
        Model info as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "models", model_id)
    header = utils.auth_header(config)
    response = create_session().get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.Model, obj_id=model_id)


def get_model_list(
    config: ClientConfig, offset: int = 0, limit: int | None = None
) -> api_pb.ModelList:
    """
    Get list of models visible to the authenticated user.


    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    offset : int
        Offset the query.
    limit : int
        Limit query response size.

    Returns
    -------
    list_pb : ModelList
        Model list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "models")
    url += utils.prepare_offset_limit_query(offset, limit)
    header = utils.auth_header(config)
    response = create_session().get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.ModelList)


def download_model_info(config: ClientConfig, model_id: str) -> api_pb.FileDownloadURL:
    """
    Get download information for a previously uploaded model.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    model_id : str
        Model ID.

    Returns
    -------
    response : api_pb.FileDownloadURL
        Download information.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "models", model_id, "download")
    header = utils.auth_header(config)
    return utils.response_as_protobuf(
        create_session().get(url, headers=header), api_pb.FileDownloadURL
    )


def _download_model(
    url: str,
    filename: str,
    dst_path: str,
    verbose: bool,
    extract_if_zipped: bool = False,
):
    """
    Download model at provided destination path and return path to the model

    Parameters
    ----------
    url : str
        Model URL to download
    filename : str
        File name of model to download
    dst_path : str
        Destination path to download model to
    verbose: bool
        Enable logs
    extract_if_zipped: bool
        If set true, extracts zipped model into provided `dst_path`

    Returns
    -------
    model_path : str
        Path to the saved model file/directory.

    Raises
    ------
        ValueError
            if zipped model does not have single base level directory.
        ValueError
            if zipped model is being extracted to a file.
    """
    extract_zipped_model = extract_if_zipped and filename.endswith(".zip")
    with tempfile.TemporaryDirectory() as tmpdir:
        # If not extracting zipped model,
        # download model at expected destination path itself.
        model_path = utils.download_file(
            url,
            filename,
            tmpdir if extract_zipped_model else dst_path,
            verbose,
            extract_if_zipped,
        )

        if not extract_zipped_model:
            return model_path

        if not os.path.isdir(dst_path):
            raise ValueError(
                "Model cannot be extracted to a file. Please provide a directory path."
            )

        # Move extracted model from temporary path to destination path
        dst_path = os.path.join(dst_path, os.path.basename(model_path))
        dst_path, _ = _get_unique_path(dst_path)

        # get_unique_path creates an empty file.
        if os.path.exists(dst_path) and os.path.isfile(dst_path):
            os.remove(dst_path)

        unzipped_model_content = os.listdir(model_path)
        if len(unzipped_model_content) != 1:
            raise ValueError("Extracted model must contain a single base model asset.")

        # Point to base model directory
        model_path = os.path.join(model_path, unzipped_model_content[0])

        shutil.copytree(model_path, dst_path)
        return dst_path


def download_model(
    config: ClientConfig,
    model_id: str,
    file_path: str,
    verbose: bool | None = None,
    extract_model: bool = False,
) -> str:
    """
    Download a previously uploaded model.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    model_id : str
        Model ID.
    file_path : str
        file location to store model to

    Returns
    -------
    model_path : str
        Path to the saved model file/directory.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    response = download_model_info(config, model_id)
    return _download_model(
        response.url,
        response.filename,
        file_path,
        verbose if verbose is not None else config.verbose,
        extract_model,
    )


def download_compiled_model(
    config: ClientConfig, job_id: str, file_path: str, verbose: bool | None = None
) -> str:
    """
    Download compiled model to file.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_id : str
        Job ID.
    file_path : str
        file location to store compiled model to

    Returns
    -------
    model_path : str
        Path to the saved model file/directory.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    # fetch compiled model
    url = utils.api_url(config, "jobs", job_id, "download_compiled_model")
    header = utils.auth_header(config)
    response = utils.response_as_protobuf(
        create_session().get(url, headers=header), api_pb.FileDownloadURL
    )
    return _download_model(
        response.url,
        response.filename,
        file_path,
        verbose if verbose is not None else config.verbose,
    )


__all__ = [
    "utils",
    "APIException",
    "ClientConfig",
    "get_auth_user",
    "get_user",
    "get_user_list",
    "get_dataset",
    "get_dataset_list",
    "get_device_list",
    "create_profile_job",
    "create_compilation_job",
    "get_job",
    "get_job_list",
    "get_job_results",
    "get_profile_job_vizgraph",
    "create_validation_job",
    "create_and_upload_dataset",
    "create_and_upload_model",
    "download_model",
    "download_compiled_model",
    "get_model",
    "get_model_list",
]


def download_dataset_info(
    config: ClientConfig, dataset_id: str
) -> api_pb.FileDownloadURL:
    """
    Get download information for a previously uploaded dataset.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    dataset_id : str
        Dataset ID.

    Returns
    -------
    response : api_pb.FileDownloadURL
        Download information.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "datasets", dataset_id, "download_data")
    header = utils.auth_header(config)
    return utils.response_as_protobuf(
        create_session().get(url, headers=header), api_pb.FileDownloadURL
    )


def download_dataset(
    config: ClientConfig, dataset_id: str, file_path: str, verbose: bool | None = None
) -> str:
    """
    Download a previously uploaded dataset.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    dataset_id : str
        Dataset ID.
    file_path : str
        file location to store model to

    Returns
    -------
    file_path : str
        Path to the saved file.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    response = download_dataset_info(config, dataset_id)
    return utils.download_file(
        response.url,
        response.filename,
        file_path,
        verbose if verbose is not None else config.verbose,
    )
