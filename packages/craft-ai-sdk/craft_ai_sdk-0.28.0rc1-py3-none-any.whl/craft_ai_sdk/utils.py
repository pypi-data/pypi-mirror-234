from datetime import datetime
from enum import Enum
import functools
from io import StringIO
import re
import sys
import xml.etree.ElementTree as ET
from requests import RequestException, Response
from json import JSONDecodeError

from .exceptions import SdkException


def handle_data_store_response(response):
    """Return the content of a response received from the datastore
    or parse the send error and raise it.

    Args:
        response (requests.Response): A response from the data store.

    Raises:
        SdkException: When the response contains an error.

    Returns:
        :obj:`str`: Content of the response.
    """
    if 200 <= response.status_code < 300:
        return response.content

    try:
        # Parse XML error returned by the data store before raising it
        xml_error_node = ET.fromstring(response.text)
        error_infos = {node.tag: node.text for node in xml_error_node}
        error_code = error_infos.pop("Code")
        error_message = error_infos.pop("Message")
        raise SdkException(
            message=error_message,
            status_code=response.status_code,
            name=error_code,
            additional_data=error_infos,
        )
    except ET.ParseError:
        raise SdkException(
            "Unable to decode response from the data store: "
            f"Content being:\n'{response.text}'",
            status_code=response.status_code,
        )


def _parse_json_response(response):
    if response.status_code == 204 or response.text == "OK":
        return
    try:
        response_json = response.json()
    except JSONDecodeError:
        raise SdkException(
            f"Unable to decode response data into json. Data being:\n'{response.text}'",
            status_code=response.status_code,
        ) from None
    return response_json


def _raise_craft_ai_error_from_response(response: Response):
    try:
        error_content = response.json()
        raise SdkException(
            message=error_content.get("message", "The server returned an error"),
            status_code=response.status_code,
            name=error_content.get("name"),
            request_id=error_content.get("request_id"),
            additional_data=error_content.get("additional_data"),
        )
    except JSONDecodeError:
        raise SdkException(
            "The server returned an invalid response content. "
            f"Content being:\n'{response.text}'",
            status_code=response.status_code,
        ) from None


def handle_http_response(response):
    if 200 <= response.status_code < 400:
        if "application/octet-stream" in response.headers.get("content-type", ""):
            return response.content
        return _parse_json_response(response)
    _raise_craft_ai_error_from_response(response)


def handle_http_request(request_func):
    def wrapper(*args, **kwargs):
        get_response = kwargs.pop("get_response", False)
        try:
            response = request_func(*args, **kwargs)
        except RequestException as error:
            raise SdkException(
                "Unable to perform the request", name="RequestError"
            ) from error

        content = handle_http_response(response)
        if get_response:
            return content, response
        return content

    return wrapper


def log_action(sdk, message, should_log=True):
    if sdk.verbose_log and should_log:
        print(message, file=sys.stderr)


def log_func_result(message, should_log=True):
    def decorator_log_func_result(action_func):
        @functools.wraps(action_func)
        def wrapper_log_func_result(*args, **kwargs):
            sdk = args[0]
            try:
                res = action_func(*args, **kwargs)
                log_action(sdk, "{:s} succeeded".format(message), should_log)
                return res
            except SdkException as error:
                log_action(
                    sdk,
                    "{:s} failed ! {}".format(message, error),
                    should_log,
                )
                raise error
            except Exception as error:
                log_action(
                    sdk,
                    "{:s} failed for unexpected reason ! {}".format(message, error),
                    should_log,
                )
                raise error

        return wrapper_log_func_result

    return decorator_log_func_result


def _datetime_to_timestamp_in_ms(dt):
    if not isinstance(dt, datetime):
        raise ValueError("Parameter must be a datetime.datetime object.")
    return int(1_000 * dt.timestamp())


def parse_isodate(date_string):
    """_summary_

    Args:
        date_string (str): date in ISO 8601 format potentially ending with
            "Z" specific character.

    Returns:
        :obj:`datetime.datetime`: A `datetime` corresponding to `date_string`.
    """
    if date_string[-1] == "Z":
        date_string = date_string.rstrip("Z")

    return datetime.fromisoformat(re.sub(r"\.\d+", "", date_string))


def use_authentication(action_func):
    @functools.wraps(action_func)
    def wrapper(sdk, *args, headers=None, **kwargs):
        actual_headers = None
        if (
            sdk._access_token_data is None
            or sdk._access_token_data["exp"]
            < (datetime.now() + sdk._access_token_margin).timestamp()
        ):
            sdk._refresh_access_token()
        actual_headers = {"Authorization": f"Bearer {sdk._access_token}"}
        if headers is not None:
            actual_headers.update(headers)

        response = action_func(sdk, *args, headers=actual_headers, **kwargs)
        if response.status_code == 401:
            sdk._clear_access_token()
        return response

    return wrapper


def remove_none_values(obj):
    return {key: value for key, value in obj.items() if value is not None}


def merge_paths(prefix, path):
    components = (value for value in path.split("/") if value != "")
    return prefix + "/".join(components)


class STEP_PARAMETER(Enum):
    """Enumeration for step parameters special values."""

    FALLBACK_PROJECT = "FALLBACK_PROJECT"
    NULL = "NULL"


def map_container_config_step_parameter(container_config):
    """
    Maps container config with :obj:`STEP_PARAMETER` enum values to final container
    config. `None` is considered to be equivalent to
    :obj:`STEP_PARAMETER.FALLBACK_PROJECT`, and should not be projected to output
    """
    ret = {}
    for key in container_config:
        val = container_config[key]
        if val is STEP_PARAMETER.NULL:
            ret[key] = None
        elif val is not STEP_PARAMETER.FALLBACK_PROJECT and val is not None:
            ret[key] = val
    return ret


# From https://stackoverflow.com/a/58767245/4839162
def chunk_buffer(buffer, size):
    size_int = int(size)
    b = buffer.read(size_int)
    while b:
        yield StringIO(b)
        b = buffer.read(size_int)


def move_branch_outside_of_container_config(step):
    """
    Moves branch out of container config and into the step itself.
    """
    container_config = step.get("container_config", {})
    repository_branch = container_config.pop("repository_branch", None)
    if repository_branch is not None:  # As we don't want to set it to None
        step["repository_branch"] = repository_branch
    return step
