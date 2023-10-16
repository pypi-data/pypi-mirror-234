from sieve.types.metadata import Metadata
from ..functions.function import _Function
from typing import Any, Optional
from sieve.api.constants import API_URL, API_BASE, V2_API_BASE
import inspect
import uuid
import os
import requests
import json
import time
from ..functions.function import get_input_names, get_output_names
from ..workflows.workflow import _Workflow
from networkx.readwrite import json_graph
from typing import Union, Dict
from ..workflows.config import Workflow
from .utils import get_config_file_path, zip_directory
from sieve.api.utils import get_api_key
from .jobs.common import JobReference
from .models.common import ModelReference
from .workflows.common import WorkflowReference
from rich import print
from rich.spinner import Spinner
from rich.live import Live
from rich.console import Console
import cloudpickle
import base64
import pickle
from pathlib import Path
from sseclient import SSEClient
import threading
from datetime import datetime


checkmark = ":white_check_mark:"
error_str = "[red bold]ERROR:[/red bold]"
success_str = "[green bold]SUCCESS:[/green bold]"
console = Console()


class BuildLogsThread(threading.Thread):
    def __init__(self, api_key, model_id, spinner):
        super().__init__()
        self.api_key = api_key
        self.model_id = model_id
        self.stop_flag = False
        self.spinner = spinner
        self.offset = int(datetime.now().timestamp() * 1e9)

    def run(self):
        headers = {}
        if self.api_key is not None:
            headers["X-API-Key"] = self.api_key

        api_url = os.getenv("SIEVE_API_URL", "https://mango.sievedata.com")
        start_streaming = False
        start_message = "pip install -r /tmp/requirements.txt"
        push_message = "The push refers to repository"
        pushing_image = False

        while not self.stop_flag:
            logs_url = f"{api_url}/{V2_API_BASE}/logs?model_id={self.model_id}&stage=build&start_time={self.offset}"
            response = requests.get(logs_url, headers=headers)
            if response.status_code != 200:
                time.sleep(2)
                continue

            logs = response.json()
            data = logs["data"]
            last_time = self.offset
            for msg in data:
                for log in msg["logs"]:
                    last_time = int(log["timestamp"]) + 1
                    log_lines = log["message"].split("\n")
                    for line in log_lines:
                        if start_message in line.strip():
                            start_streaming = True
                        if push_message in line.strip():
                            self.spinner.update(text=f"Pushing image...")
                            pushing_image = True
                            continue

                        if (
                            line.strip() == ""
                            or line == "\n"
                            or not start_streaming
                            or pushing_image
                        ):
                            continue
                        console.print("[yellow]" + line + "[/yellow]", highlight=False)
                        time.sleep(0.01)

            self.offset = last_time
            time.sleep(2)

    def stop(self):
        self.stop_flag = True


def upload(a: Any, version: str = None, API_KEY: str = None, single_build: bool = True):
    """
    Decorator to upload a Sieve model or function to the cloud.

    :param a: Model or function to upload
    :type a: Any
    :param version: Version of the model or function to upload
    :type version: str
    :param API_KEY: API key to use for authentication
    :type API_KEY: str
    :param single_build: If true, print a link to the model after building
    :type single_build: bool
    """
    api_key = get_api_key(API_KEY)

    _Function.upload = True
    if version is None:
        version = str(uuid.uuid4())
    model_name = a.name

    spin = Spinner("dots", text=f"Uploading {model_name}...")
    live = Live(spin, refresh_per_second=10, console=console)
    live.start()

    if isinstance(a, _Function):
        tmp_config = {}
        tmp_config["name"] = a.name
        tmp_config["python_packages"] = a.python_packages
        tmp_config["system_packages"] = a.system_packages
        tmp_config["filepath"] = a.relative_path
        tmp_config["inputs"] = get_input_names(a)
        tmp_config["outputs"] = get_output_names(a)
        tmp_config["version"] = version
        tmp_config["python_version"] = a.python_version
        tmp_config["cuda_version"] = a.cuda_version
        tmp_config["system_version"] = a.system_version
        tmp_config["local_name"] = a.local_name
        tmp_config["is_iterator_input"] = a.is_iterator_input
        tmp_config["persist_output"] = a.persist_output
        tmp_config["is_iterator_output"] = inspect.isgeneratorfunction(a.function)
        tmp_config["type"] = "function"
        tmp_config["run"] = a.run_commands
        tmp_config["env"] = get_env_list_dict(a.environment_variables)
        tmp_config["public_data"] = process_metadata(a.metadata, api_key)
        if a.machine_type:
            tmp_config["machine_type"] = a.machine_type
            tmp_config["gpu"] = str(a.gpu != "cpu").lower()
        elif isinstance(a.gpu, bool):
            tmp_config["machine_type"] = "T4" if a.gpu else "cpu"
            tmp_config["gpu"] = str(a.gpu).lower()
        else:
            tmp_config["machine_type"] = a.gpu
            tmp_config["gpu"] = str(a.gpu != "cpu").lower()
        config = {}
        for a, val in tmp_config.items():
            if val is not None:
                config[a] = val

    else:
        tmp_config = {}
        tmp_config["name"] = a.name
        tmp_config["gpu"] = str(a.gpu).lower()
        tmp_config["python_packages"] = a.python_packages
        tmp_config["system_packages"] = a.system_packages
        tmp_config["filepath"] = a.relative_path
        tmp_config["inputs"] = get_input_names(a.function)
        tmp_config["outputs"] = get_output_names(a.function)
        tmp_config["version"] = version
        tmp_config["python_version"] = a.python_version
        tmp_config["cuda_version"] = a.cuda_version
        tmp_config["system_version"] = a.system_version
        tmp_config["local_name"] = a.local_name
        tmp_config["is_iterator_input"] = a.function.is_iterator_input
        tmp_config["persist_output"] = a.function.persist_output
        tmp_config["is_iterator_output"] = inspect.isgeneratorfunction(
            a.function.function
        )
        tmp_config["type"] = "model"
        tmp_config["run"] = a.function.run_commands
        tmp_config["env"] = get_env_list_dict(a.environment_variables)
        tmp_config["public_data"] = process_metadata(a.metadata, api_key)
        if a.machine_type:
            tmp_config["machine_type"] = a.machine_type
            tmp_config["gpu"] = str(a.gpu != "cpu").lower()
        elif isinstance(a.gpu, bool):
            tmp_config["machine_type"] = "T4" if a.gpu else "cpu"
            tmp_config["gpu"] = str(a.gpu).lower()
        else:
            tmp_config["machine_type"] = a.gpu
            tmp_config["gpu"] = str(a.gpu != "cpu").lower()
        config = {}
        for a, val in tmp_config.items():
            if val is not None:
                config[a] = val

    parent_path = str(Path(config["filepath"]).parents[0])
    zip_path = zip_directory(parent_path, os.path.join(parent_path, "archive.zip"))

    upload_url_url = f"{API_URL}/{API_BASE}/upload_url"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }
    payload = {"file_name": str(uuid.uuid4())}

    upload_response = requests.request(
        "POST", upload_url_url, headers=headers, json=payload
    )

    upload_url_json = upload_response.json()
    upload_url = upload_url_json["upload_url"]
    headers = {"x-goog-content-length-range": "0,10000000000"}
    file_upload_response = requests.request(
        "PUT", upload_url, headers=headers, data=open(zip_path, "rb")
    )

    url = f"{API_URL}/{API_BASE}/models/upload"
    payload = {"dir_url": upload_url_json["get_url"], "config": config}
    headers = {
        "X-API-KEY": api_key,
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    os.remove(zip_path)

    if 200 <= response.status_code < 300:
        model_id = response.json()["id"]
        thread = BuildLogsThread(api_key, model_id, spin)
        thread.daemon = True
        thread.start()

        out = requests.get(
            f"{API_URL}/{V2_API_BASE}/user/organization", headers=headers
        )
        if 200 <= out.status_code < 300:
            user_info = out.json()
            name = user_info["name"]
            spin.update(text=f"Building {model_name}...")
            _Function.upload = False

            model = ModelReference(
                id=model_id, name=model_name, version=version, owner=name
            )
            curr_status = model.status()
            while curr_status != "ready":
                if curr_status == "error":
                    print(
                        f"\n{error_str} There was an issue building your model. View logs with `sieve model info {model_id}`"
                    )
                    return
                time.sleep(1)
                curr_status = model.status()

            thread.stop()
            live.update(f"[green]:heavy_check_mark:[/green] Deployed {model_name}\n")
            live.stop()

            if single_build:
                print(
                    "Your model has been built. Your model id is "
                    + model_id
                    + f". Your model version is {version}. You can check the status of your model at https://sievedata.com/app/"
                    + name
                    + "/models"
                )
            return model
        else:
            print(
                f"There was an issue retrieving your user info, but your model with id {model_id} should be processing:"
                + out.text
            )

        return ModelReference(id=model_id, name=model_name, version=version, owner=None)
    if 400 <= response.status_code < 500:
        print(
            f"\n{error_str} There was an issue processing your model: {response.text}"
        )
    if 500 <= response.status_code < 600:
        print(
            f"\n{error_str} There was an issue processing your model: {response.text}"
        )
    # else:
    #     raise TypeError("Invalid argument to upload", a)
    _Function.upload = False


def deploy(workflow: _Workflow, API_KEY: str = None):
    """
    Decorator to deploy a workflow to the cloud.

    :param workflow: Workflow to deploy
    :type workflow: _Workflow
    :param API_KEY: API key to use for authentication
    :type API_KEY: str
    :return: Workflow reference for you to track the workflow with
    :rtype: WorkflowReference
    """
    api_key = get_api_key(API_KEY)

    if not issubclass(type(workflow), _Workflow):
        raise TypeError("Invalid argument to deploy", workflow)

    print(f"Deploying workflow {workflow.name}...", end="", flush=True)

    graph = workflow()
    graph_dict = json_graph.node_link_data(graph)
    wk = Workflow(config=graph_dict, name=workflow.name)
    data = wk.dict(by_alias=True)
    data["public_data"] = process_metadata(workflow.metadata, api_key)
    url = f"{API_URL}/{API_BASE}/workflows/{workflow.name}"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, json=data)
    if 200 <= response.status_code < 300:
        print(checkmark)
        return WorkflowReference(id=response.json()["id"], name=workflow.name)
    if response.status_code == 400:
        print(f"\nWorkflow already exists, attempting to edit...", end="", flush=True)
        url = f"{API_URL}/{API_BASE}/workflows/{workflow.name}"
        response = requests.request("PUT", url, headers=headers, json=data)
        if 200 <= response.status_code < 300:
            print(checkmark)
            return WorkflowReference(id=response.json()["id"], name=workflow.name)
        if 400 <= response.status_code < 500:
            print(
                f"\n{error_str} There was an issue editing your workflow: {response.text}"
            )
    if 401 <= response.status_code < 600:
        print(
            f"\n{error_str} There was an issue processing your workflow: {response.text}"
        )
    print()
    return


def delete(workflow: _Workflow, KEY: str = None):
    """
    Decorator to delete a workflow from the cloud.

    :param workflow: Workflow to delete
    :type workflow: _Workflow
    :param API_KEY: API key to use for authentication
    :type API_KEY: str
    """

    api_key = get_api_key(KEY)
    if not issubclass(type(workflow), _Workflow):
        raise TypeError("Invalid argument to deploy", workflow)

    graph = workflow()
    graph_dict = json_graph.node_link_data(graph)
    wk = Workflow(config=graph_dict, name=workflow.name)
    data = wk.dict()
    url = f"{API_URL}/{API_BASE}/workflows/{workflow.name}"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }
    response = requests.request("DELETE", url, headers=headers, json=data)
    if 200 <= response.status_code < 300:
        print("Your workflow has been deleted!")
    if 400 <= response.status_code < 500:
        print("There was an issue processing your workflow. " + response.text)
    if 500 <= response.status_code < 600:
        print("There was an issue processing your workflow. " + response.text)


def push(
    workflow: Optional[Union[_Workflow, str]] = None,
    model_id: Optional[str] = None,
    inputs: Dict[str, Any] = None,
    API_KEY: str = None,
    wait: bool = False,
    env: Dict[str, str] = {},
):
    """
    Decorator to push inputs to a workflow or model

    :param workflow: Workflow to push inputs to
    :type workflow: _Workflow
    :param model_id: Model id to push inputs to
    :type model_id: str
    :param inputs: Inputs to push to workflow or model
    :type inputs: Dict[str, Any]
    :param API_KEY: API key to use for authentication
    :type API_KEY: str
    :param wait: Whether to wait for the job to finish
    :type wait: bool
    :param env: Environment variables to use for the job
    :type env: Dict[str, str]
    :return: Job reference for you to track the job with
    :rtype: JobReference
    """

    api_key = get_api_key(API_KEY)

    if model_id is None and workflow is None:
        raise ValueError("Must specify either model_id or workflow")
    if model_id is not None and workflow is not None:
        raise ValueError("Cannot specify both model_id and workflow")

    parent = os.environ.get("SIEVE_JOB_ID", "")

    url = f"{API_URL}/{V2_API_BASE}/push"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    pickled_inputs = {}
    for key, value in inputs.items():
        pickled_inputs[key] = base64.b64encode(cloudpickle.dumps(value)).decode("ascii")

    data = {"inputs": pickled_inputs, "env": env, "serialized": True, "parent": parent}
    if model_id is not None:
        data["model"] = model_id
    else:
        if type(workflow) == str:
            workflow_name = workflow
        else:
            if not issubclass(type(workflow), _Workflow):
                raise TypeError("Invalid argument to push", workflow)
            workflow_name = workflow.name
        data["workflow"] = workflow_name
    response = requests.request("POST", url, headers=headers, json=data)
    if 200 <= response.status_code < 300:
        rjson = response.json()
        jid = rjson["id"]
        print(f"Pushed job with id={jid} {checkmark}")

        job_ref = JobReference(id=jid)
        if not wait:
            return job_ref
        curr_status = job_ref.status()
        while curr_status != "finished":
            if curr_status == "error":
                print(
                    f"\n{error_str} There was an issue with your job. Please run `sieve job get {jid}` to get detailed logs"
                )
                return
            time.sleep(1)
            curr_status = job_ref.status()

        print(f"{success_str} Finished job successfully {checkmark}\n")
        return JobReference(id=jid)
    if 400 <= response.status_code < 500:
        print(f"\n{error_str}There was an issue processing your job: {response.text}")
    if 500 <= response.status_code < 600:
        print(f"\n{error_str}There was an issue processing your job: {response.text}")


def get(job_id=None, API_KEY=None, limit=10000, offset=0):
    """
    Query jobs from the API

    :param job_id: Job id to query logs for
    :type job_id: str
    :param API_KEY: API key to use for authentication
    :type API_KEY: str
    :param limit: Number of logs to return
    :type limit: int
    :param offset: Offset to start from
    :type offset: int
    :return: Jobs
    :rtype: dict
    """

    api_key = get_api_key(API_KEY)
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }

    # Get the pickled outputs for client
    r = requests.get(
        f"{API_URL}/{API_BASE}/jobs/{job_id}",
        params={"raw_data": 1, "limit": limit, "offset": offset},
        headers=headers,
    )
    rjson = r.json()

    obj_results = []
    for res in rjson["data"]:
        unpickled_out = pickle.loads(base64.b64decode(res["output"]))
        obj_results.append(unpickled_out)
    rjson["data"] = obj_results
    return rjson


def logs(
    job_id=None,
    model_id=None,
    workflow_id=None,
    id=None,
    API_KEY=None,
    limit=100,
    offset=b"",
):
    """
    Query logs from the API

    :param job_id: Job id to query logs for
    :type job_id: str
    :param model_id: Model id to query logs for
    :type model_id: str
    :param workflow_id: Workflow id to query logs for
    :type workflow_id: str
    :param id: id to query logs for in case of a single log
    :type id: str
    :param API_KEY: API key to use for authentication
    :type API_KEY: str
    :param limit: Number of logs to return
    :type limit: int
    :param offset: Offset to start from
    :type offset: bytes
    :return: Logs
    :rtype: dict
    """

    api_key = get_api_key(API_KEY)
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }
    r = requests.get(
        f"{API_URL}/{API_BASE}/logs",
        params={
            "job_id": job_id,
            "model_id": model_id,
            "workflow_id": workflow_id,
            "id": id,
            "limit": limit,
            "offset": offset,
        },
        headers=headers,
    )
    rjson = r.json()
    return rjson


def upload_file(
    api_key: str, file_name: str, public_upload: bool, public_request: bool, file
):
    """
    Upload file to GCS and return authenticated (or public) URL
    :param api_key: API key to use for authentication
    :type api_key: str
    :param file_name: Name of file to upload (optional)
    :type file_name: str
    :param public_upload: Whether to upload the file publicly
    :type public_upload: bool
    :param public_request: Whether this is a public request (no auth). Used for public demos.
    :type public_request: bool
    :param file: File to upload
    :type file: file
    """
    endpoint = os.getenv("SIEVE_API_URL", "https://mango.sievedata.com")
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }

    data = {
        "file_name": file_name or f"{uuid.uuid4()}",
        "public": public_upload,
        "public_upload": public_request,
    }

    res = requests.post(
        f"{endpoint}/v1/upload_url", headers=headers, data=json.dumps(data)
    )

    json_res = res.json()

    upload_headers = {
        "x-goog-content-length-range": "0,10000000000",
    }

    upload_res = requests.put(json_res["upload_url"], data=file, headers=upload_headers)
    file.close()
    return json_res.get("get_url")


def process_metadata(metadata: Metadata, api_key: str):
    """
    Upload public data to cloud storage if needed and return public data struct
    :param metadata: Metadata to process
    :type metadata: Metadata
    :param api_key: API key to use for authentication
    :type api_key: str
    """
    if metadata is None:
        return {}

    public_data = metadata.dict()

    if metadata.image is not None:
        public_data["image"] = upload_file(
            api_key,
            file_name=None,
            public_upload=True,
            public_request=False,
            file=open(metadata.image.path, "rb"),
        )
    return public_data


def get_env_list_dict(env_list):
    """Get a list of env vars as a dict"""
    try:
        return [i.dict() for i in env_list]
    except:
        raise TypeError(
            "Badly supplied env vars, make sure you supply a list of sieve.Env config variables",
            env_list,
        )


def whoami(API_KEY=None):
    api_key = get_api_key(API_KEY)
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }

    r = requests.get(f"{API_URL}/{API_BASE}/auth/user", headers=headers)
    data = r.json()
    data["status"] = r.status_code

    r_org = requests.get(f"{API_URL}/{V2_API_BASE}/user/organization", headers=headers)
    data_org = r_org.json()

    return {**data, **data_org}


def write_key(key: str):
    """
    This function writes the api key to the config file.
    """
    path = get_config_file_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(key)
