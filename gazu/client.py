import functools
import json
import shutil
import urllib

from .encoder import CustomJSONEncoder

from .exception import (
    TooBigFileException,
    NotAuthenticatedException,
    NotAllowedException,
    MethodNotAllowedException,
    ParameterException,
    RouteNotFoundException,
    ServerErrorException,
    UploadFailedException,
)


class KitsuClient(object):
    def __init__(self, host):
        self.tokens = {"access_token": "", "refresh_token": ""}
        self.session = requests.Session()
        self.host = host
        self.event_host = host


def create_client(host):
    return KitsuClient(host)


default_client = None
try:
    import requests

    # Little hack to allow json encoder to manage dates.
    requests.models.complexjson.dumps = functools.partial(
        json.dumps, cls=CustomJSONEncoder
    )
    host = "http://gazu.change.serverhost/api"
    default_client = create_client(host)
except:
    print("Warning, running in setup mode!")


def host_is_up(client=default_client):
***REMOVED***
    Returns:
        True if the host is up.
***REMOVED***
    try:
        response = client.session.head(client.host)
    except:
***REMOVED***
    return response.status_code == 200


def host_is_valid(client=default_client):
***REMOVED***
    Check if the host is valid by simulating a fake login.
    Returns:
        True if the host is valid.
***REMOVED***
    if not host_is_up(client):
***REMOVED***
    try:
        post("auth/login", {"email": "", "password": ""})
    except Exception as exc:
        return type(exc) == ParameterException


def get_host(client=default_client):
***REMOVED***
    Returns:
        Host on which requests are sent.
***REMOVED***
    return client.host


def get_api_url_from_host(client=default_client):
***REMOVED***
    Returns:
        Zou url, retrieved from host.
***REMOVED***
    return client.host[:-4]


def set_host(new_host, client=default_client):
***REMOVED***
    Returns:
        Set currently configured host on which requests are sent.
***REMOVED***
    client.host = new_host
    return client.host


def get_event_host(client=default_client):
***REMOVED***
    Returns:
        Host on which listening for events.
***REMOVED***
    return client.event_host or client.host


def set_event_host(new_host, client=default_client):
***REMOVED***
    Returns:
        Set currently configured host on which listening for events.
***REMOVED***
    client.event_host = new_host
    return client.event_host


def set_tokens(new_tokens, client=default_client):
***REMOVED***
    Store authentication token to reuse them for all requests.

    Args:
        new_tokens (dict): Tokens to use for authentication.
***REMOVED***
    client.tokens = new_tokens
    return client.tokens


def make_auth_header(client=default_client):
***REMOVED***
    Returns:
        Headers required to authenticate.
***REMOVED***
    if "access_token" in client.tokens:
        return {"Authorization": "Bearer %s" % client.tokens["access_token"]}
***REMOVED***
        return {}


def url_path_join(*items):
***REMOVED***
    Make it easier to build url path by joining every arguments with a '/'
    character.

    Args:
        items (list): Path elements
***REMOVED***
    return "/".join([item.lstrip("/").rstrip("/") for item in items])


def get_full_url(path, client=default_client):
***REMOVED***
    Args:
        path (str): The path to integrate to host url.

    Returns:
        The result of joining configured host url with given path.
***REMOVED***
    return url_path_join(get_host(client), path)


def build_path_with_params(path, params):
***REMOVED***
    Add params to a path using urllib encoding

    Args:
        path (str): The url base path
        params (dict): The parameters to add as a dict

    Returns:
        str: the builded path
***REMOVED***
    if not params:
        return path

    if hasattr(urllib, "urlencode"):
        path = "%s?%s" % (path, urllib.urlencode(params))
***REMOVED***
        path = "%s?%s" % (path, urllib.parse.urlencode(params))
    return path


def get(path, json_response=True, params=None, client=default_client):
***REMOVED***
    Run a get request toward given path for configured host.

    Returns:
        The request result.
***REMOVED***
    path = build_path_with_params(path, params)

    response = client.session.get(
        get_full_url(path, client=client),
        headers=make_auth_header(client=client)
    )
    check_status(response, path)

    if json_response:
        return response.json()
***REMOVED***
        return response.text


def post(path, data, client=default_client):
***REMOVED***
    Run a post request toward given path for configured host.

    Returns:
        The request result.
***REMOVED***
    response = client.session.post(
        get_full_url(path, client), json=data,
        headers=make_auth_header(client=client)
    )
    check_status(response, path)
    return response.json()


def put(path, data, client=default_client):
***REMOVED***
    Run a put request toward given path for configured host.

    Returns:
        The request result.
***REMOVED***
    response = client.session.put(
        get_full_url(path, client),
        json=data,
        headers=make_auth_header(client=client)
    )
    check_status(response, path)
    return response.json()


def delete(path, params=None, client=default_client):
***REMOVED***
    Run a get request toward given path for configured host.

    Returns:
        The request result.
***REMOVED***
    path = build_path_with_params(path, params)

    response = client.session.delete(
        get_full_url(path, client),
        headers=make_auth_header(client=client)
    )
    check_status(response, path)
    return response.text


def check_status(request, path):
***REMOVED***
    Raise an exception related to status code, if the status code does not match
    a success code. Print error message when it's relevant.

    Args:
        request (Request): The request to validate.

    Returns:
        int: Status code

    Raises:
        ParameterException: when 400 response occurs
        NotAuthenticatedException: when 401 response occurs
        RouteNotFoundException: when 404 response occurs
        NotAllowedException: when 403 response occurs
        MethodNotAllowedException: when 405 response occurs
        TooBigFileException: when 413 response occurs
        ServerErrorException: when 500 response occurs
***REMOVED***
    status_code = request.status_code
    if status_code == 404:
        raise RouteNotFoundException(path)
    elif status_code == 403:
        raise NotAllowedException(path)
    elif status_code == 400:
        text = request.json().get("message", "No additional information")
        raise ParameterException(path, text)
    elif status_code == 405:
        raise MethodNotAllowedException(path)
    elif status_code == 413:
        raise TooBigFileException(
            "%s: You send a too big file. "
            "Change your proxy configuration to allow bigger files." % path
***REMOVED***
    elif status_code in [401, 422]:
        raise NotAuthenticatedException(path)
    elif status_code in [500, 502]:
***REMOVED***
            stacktrace = request.json().get(
                "stacktrace", "No stacktrace sent by the server"
    ***REMOVED***
            message = request.json().get(
                "message", "No message sent by the server"
    ***REMOVED***
            print("A server error occured!\n")
            print("Server stacktrace:\n%s" % stacktrace)
            print("Error message:\n%s\n" % message)
***REMOVED***
            print(request.text)
        raise ServerErrorException(path)
    return status_code


def fetch_all(path, params=None, client=default_client):
***REMOVED***
    Args:
        path (str): The path for which we want to retrieve all entries.

    Returns:
        list: All entries stored in database for a given model. You can add a
        filter to the model name like this: "tasks?project_id=project-id"
***REMOVED***
    return get(url_path_join("data", path), params=params, client=client)


def fetch_first(path, params=None, client=default_client):
***REMOVED***
    Args:
        path (str): The path for which we want to retrieve the first entry.

    Returns:
        dict: The first entry for which a model is required.
***REMOVED***
    entries = get(url_path_join("data", path), params=params, client=client)
    if len(entries) > 0:
        return entries[0]
***REMOVED***
        return None


def fetch_one(model_name, id, client=default_client):
***REMOVED***
    Function dedicated at targeting routes that returns a single model instance.

    Args:
        model_name (str): Model type name.
        id (str): Model instance ID.

    Returns:
        dict: The model instance matching id and model name.
***REMOVED***
    return get(url_path_join("data", model_name, id), client=client)


def create(model_name, data, client=default_client):
***REMOVED***
    Create an entry for given model and data.

    Returns:
        dict: Created entry
***REMOVED***
    return post(url_path_join("data", model_name), data, client=client)


def upload(path, file_path, data={}, extra_files=[], client=default_client):
***REMOVED***
    Upload file located at *file_path* to given url *path*.

    Args:
        path (str): The url path to upload file.
        file_path (str): The file location on the hard drive.

    Returns:
        Response: Request response object.
***REMOVED***
    url = get_full_url(path, client)
    files = _build_file_dict(file_path, extra_files)
    response = client.session.post(
        url,
        data=data,
        headers=make_auth_header(client=client),
        files=files
    )
    check_status(response, path)
***REMOVED*** = response.json()
    if "message" in result:
        raise UploadFailedException(result["message"])
    return result


def _build_file_dict(file_path, extra_files):
    files = {"file": open(file_path, "rb")}
    i = 2
    for file_path in extra_files:
        files["file-%s" % i] = open(file_path, "rb")
        i += 1
    return files


def download(path, file_path, client=default_client):
***REMOVED***
    Download file located at *file_path* to given url *path*.

    Args:
        path (str): The url path to download file from.
        file_path (str): The location to store the file on the hard drive.

    Returns:
        Response: Request response object.

***REMOVED***
    url = get_full_url(path, client)
    with client.session.get(
        url,
        headers=make_auth_header(client=client),
        stream=True
    ) as response:
        with open(file_path, "wb") as target_file:
            shutil.copyfileobj(response.raw, target_file)


def get_file_data_from_url(url, full=False, client=default_client):
***REMOVED***
    Return data found at given url.
***REMOVED***
    if not full:
        url = get_full_url(url)
    response = requests.get(
        url,
        stream=True,
        headers=make_auth_header(client=client),
        client=client
    )
    check_status(response, url)
    return response


def import_data(model_name, data, client=default_client):
***REMOVED***
    Args:
        model_name (str): The data model to import
        data (dict): The data to import
***REMOVED***
    return post("/import/kitsu/%s" % model_name, data, client=client)


def get_api_version(client=default_client):
***REMOVED***
    Returns:
        str: Current version of the API.
***REMOVED***
    return get("", client)["version"]


def get_current_user(client=default_client):
***REMOVED***
    Returns:
        dict: User database information for user linked to auth tokens.
***REMOVED***
    return get("auth/authenticated", client)["user"]
