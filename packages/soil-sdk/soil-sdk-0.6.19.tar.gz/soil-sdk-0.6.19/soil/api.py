"""
This package contains calls to the SOIL's REST API
"""
import json
import logging
from typing import Any, Dict, List, Optional, TypedDict
from urllib.parse import urlencode
import requests
from requests import Response
from requests.adapters import HTTPAdapter, Retry
from soil import errors
from soil.configuration import GLOBAL_CONFIG
from soil.types import Experiment, GetModule, Plan, Result, GetModuleHash

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

API_ROOT = f"{str(GLOBAL_CONFIG.host)}/v2/"


class _SoilSession(requests.Session):
    """Creates a Soil session that will refresh the token when necessary."""

    def _add_header(self) -> None:
        self.headers.update({"Authorization": f"Bearer {str(GLOBAL_CONFIG.token)}"})

    def get(self, *args, **kwargs) -> Response:
        self._add_header()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs) -> Response:
        self._add_header()
        return super().post(*args, **kwargs)

    def put(self, *args, **kwargs) -> Response:
        self._add_header()
        return super().put(*args, **kwargs)

    def patch(self, *args, **kwargs) -> Response:
        self._add_header()
        return super().patch(*args, **kwargs)


def _setup_requests_session() -> _SoilSession:
    """Creates a requests session object to be reused in the API calls."""
    _session = _SoilSession()
    _session.headers.update(
        {
            "Content-Type": "application/json",
        }
    )
    # Retries at 2, 4, 8, 16, 32 seconds
    retries = Retry(
        total=5, backoff_factor=2, status_forcelist=[500, 501, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    _session.mount("http://", adapter)
    _session.mount("https://", adapter)
    return _session


session = _setup_requests_session()


def upload_data(dtype: str, data: Any, metadata: Any) -> Result:
    """Upload data to the cloud as a new dataset."""
    logger.debug("upload_data:%s")
    url = API_ROOT + "results/"
    body = {"type": dtype, "data": data, "metadata": metadata}
    response = session.post(url, json=body, timeout=30)
    if response.status_code != 201:
        raise errors.DataNotUploaded(response.text)
    return json.loads(response.text)


def get_result(result_id: str) -> Dict[str, Any]:
    """Get the result data"""
    logger.debug("get_result:%s", result_id)
    url = API_ROOT + "results/" + result_id + "/"
    response = session.get(url, timeout=30)
    if response.status_code != 200:
        raise errors.DataNotFound(response.text)
    return json.loads(response.text)


def get_result_data(
    result_id: str, query: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Get the result data"""
    if query is None:
        query = {}
    logger.debug("get_result:%s %s", result_id, str(query))
    url = API_ROOT + "results/" + result_id + "/data/?" + urlencode(query)
    response = session.get(url, timeout=30)
    if response.status_code != 200:
        raise errors.DataNotFound(response.text)
    return json.loads(response.text)


def export_result(
    result_id: str, file_path: str, query: Optional[Dict[str, str]] = None
) -> None:
    """Export result and saves it to a file"""
    if query is None:
        query = {}
    logger.debug("export_result:%s %s", result_id, str(query))
    url = API_ROOT + "results/" + result_id + "/export/?" + urlencode(query)
    response = session.get(url, timeout=30)
    if response.status_code != 200:
        raise errors.DataNotFound(response.text)
    with open(file_path, "wb") as fd:
        fd.write(response.content)


class _SoilUploadModule(TypedDict):
    name: str
    code: str
    is_package: bool


def upload_modules(modules: list[_SoilUploadModule]) -> None:
    """Uploads a chunk of modules"""
    logger.debug("upload_modules:%s", modules)
    url = API_ROOT + "modules/"
    data = {"modules": modules}
    response = session.post(url, json=data, timeout=30)
    if response.status_code != 200:
        raise errors.ModuleNotUploaded(response.text)


def upload_module(module_name: str, code: str, is_package: bool) -> None:
    """Uploads a module"""
    logger.debug("upload_module:%s", module_name)
    url = API_ROOT + "modules/"
    data = {"name": module_name, "code": code, "is_package": is_package}
    response = session.post(url, json=data, timeout=30)
    if response.status_code != 200:
        raise errors.ModuleNotUploaded(response.text)


def get_module(full_name: str) -> GetModule:
    """Downloads a module"""
    logger.debug("get_module:%s", full_name)
    url = API_ROOT + "modules/" + full_name + "/"
    response = session.get(url, timeout=30)
    if response.status_code != 200:
        raise errors.ModuleNotFound(response.text)
    return json.loads(response.text)


def get_modules() -> list[GetModuleHash]:
    """Gets a list"""
    logger.debug("get_module:%s")
    url = f"{API_ROOT}modules/"
    response = session.get(url, timeout=30)
    if response.status_code != 200:
        raise errors.ModuleNotFound(response.text)
    return json.loads(response.text)["result"]


def set_alias(alias: str, result_id: str, roles: Optional[List[str]] = None) -> None:
    """Sets an alias for a result. Updates a previous one with the same name."""
    logger.debug("set_alias: %s = %s", alias, result_id)
    obj = {"name": alias, "state": {"alias": alias, "result_id": result_id}}
    if roles is not None:
        obj["roles"] = roles
    try:
        old_alias_id = get_alias(alias)["_id"]
        url = API_ROOT + "states/" + old_alias_id + "/"
        response = session.patch(url, json=obj, timeout=30)
    except errors.DataNotFound:
        url = API_ROOT + "states/"
        response = session.post(url, json=obj, timeout=30)
    if response.status_code != 200:
        raise errors.DataNotUploaded(f"Failed to create alias {alias}: {response.text}")

    if roles is not None:
        url = API_ROOT + "results/" + result_id + "/"
        response = session.patch(url, json={"roles": roles}, timeout=30)
        if response.status_code != 200:
            raise errors.DataNotUploaded(
                f"Failed to patch result {result_id}: {response.text}"
            )


def get_alias(alias: str) -> Dict[str, Any]:
    """Gets an alias"""
    logger.debug("get_alias: %s", alias)
    url = API_ROOT + "states/?name=" + alias + "&with-roles"
    response = session.get(url, timeout=30)
    if response.status_code != 200:
        raise errors.ObjectNotFound("Error getting alias:" + response.text)
    aliases = json.loads(response.text)
    if len(aliases) == 0:
        raise errors.DataNotFound("Alias not found")
    alias_id = aliases[0]["_id"]
    url = API_ROOT + "states/" + alias_id + "/"
    response = session.get(url, timeout=30)
    if response.status_code != 200:
        raise errors.ObjectNotFound("Error getting alias with id " + response.text)
    return json.loads(response.text)


def create_experiment(plan: Plan) -> Experiment:
    """Runs an experiment in SOIL"""
    logger.debug("create_experiment: %s", str(plan))
    url = API_ROOT + "experiments/"
    experiment = {"name": "", "description": "", "plan": plan}
    response = session.post(url, json={"experiment": experiment}, timeout=30)
    if response.status_code != 200:
        raise ValueError("Error creating the experiment:" + response.text)
    return json.loads(response.text)["experiment"]


def get_experiment(experiment_id: str) -> Experiment:
    """Runs an experiment from SOIL"""
    logger.debug("get_experiment: %s", experiment_id)
    url = API_ROOT + "experiments/" + experiment_id + "/"
    response = session.get(url, timeout=30)
    if response.status_code != 200:
        raise ValueError(
            "Error getting the experiment " + experiment_id + "\n" + response.text
        )
    return json.loads(response.text)


def get_experiment_logs(experiment_id: str, start_date: str) -> Any:
    """Gets logs from a SOIL experiment"""
    logger.debug("get_experiment_id: %s since %s", experiment_id, start_date)
    url = (
        API_ROOT
        + "experiments/"
        + experiment_id
        + "/logs/?"
        + urlencode({"start_date": start_date})
    )
    response = session.get(url, timeout=30)
    if response.status_code != 200:
        raise ValueError(
            "Error getting the experiment " + experiment_id + "\n" + response.text
        )
    return json.loads(response.text)


def create_event(key: str, value: Any) -> Any:
    """Saves an event in soil"""
    url = API_ROOT + "alerts/events/"
    response = session.post(url, json={"key": key, "value": value}, timeout=30)
    if response.status_code != 201:
        raise errors.EventNotUploaded("Error saving the event:" + response.text)
    return json.loads(response.text)


def create_alert(alert: Dict) -> Any:
    """Creates an alert"""
    url = API_ROOT + "alerts/alerts/"
    response = session.post(url, json=alert, timeout=30)
    if response.status_code != 201:
        raise errors.AlertNotUploaded("Error creating the alert:" + response.text)
    return json.loads(response.text)


def get_dictionary(name: str, language: str) -> Dict[str, Any]:
    """Get the a dictionary"""
    url = API_ROOT + "dictionaries/" + name + "/?language=" + language
    response = session.get(url, timeout=30)
    if response.status_code != 200:
        raise errors.DictionaryNotFound("Error getting dictionary:" + response.text)
    return json.loads(response.text)


def create_dictionary(name: str, language: str, content: Dict) -> Dict[str, Any]:
    """Create a dictionary or update it"""
    logger.debug("create_dictionary: %s in language: %s", str(name), str(language))

    try:
        dictionary = get_dictionary(name, language)
        dictionary_exists = dictionary["language"] == language
    except errors.DictionaryNotFound:
        dictionary_exists = False

    data = {
        "name": name,
        "language": language,
        "content": content,
    }

    if dictionary_exists:
        url = f"{API_ROOT}dictionaries/{name}/"
        response = session.patch(url, json=data, timeout=30)
    else:
        url = f"{API_ROOT}dictionaries/"
        response = session.post(url, json=data, timeout=30)

    if response.status_code != 200:
        raise errors.DictionaryNotUploaded(
            f"Error creating/updating the dictionary {name} in language {language}: {response.text}"
        )
    return json.loads(response.text)
