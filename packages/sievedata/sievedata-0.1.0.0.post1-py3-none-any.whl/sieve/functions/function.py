import inspect
from sieve.api.utils import get_api_key_no_error, get_api_key

from ..types.base import Struct
import inspect
from typing import Dict, Any, List, Optional
import os
import networkx as nx
import uuid
from .utils import type_to_str, _issubclass, type_to_schema
from pydantic import BaseModel
import docstring_parser
from ..types.metadata import Metadata
from ..api.constants import API_BASE, V2_API_BASE
import requests
import concurrent.futures
import base64
import cloudpickle
import grpc
from ..server.proto import server_pb2_grpc
from ..server.proto import server_pb2
import time
from ..server.logging.logging import get_sieve_internal_logger
import json
import threading
from sseclient import SSEClient
from rich import print
from rich.console import Console
from ..server.handling.file_handling import get_global_handler
from datetime import datetime

sieve_internal_logger = get_sieve_internal_logger()
console = Console()


class InvalidFunctionException(Exception):
    pass


class InvalidModelException(Exception):
    pass


class InvalidGraphException(Exception):
    pass


class InvalidTypeException(Exception):
    pass


# TODO: Change to something more foolproof
def is_local():
    if os.environ.get("SIEVE_JOB_ID") is not None:
        return False
    return True


class Env(BaseModel):
    name: str
    default: str = None
    description: str = None


class JobLogsThread(threading.Thread):
    def __init__(self, api_key, job_id):
        super().__init__()
        self.api_key = api_key
        self.job_id = job_id
        self.stop_flag = False
        self.offset = int(datetime.now().timestamp() * 1e9)

    def run(self):
        headers = {}
        if self.api_key is not None:
            headers["X-API-Key"] = self.api_key

        api_url = os.getenv("SIEVE_API_URL", "https://mango.sievedata.com")

        while not self.stop_flag:
            logs_url = f"{api_url}/{V2_API_BASE}/logs?job_id={self.job_id}&start_time={self.offset}"
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
                    console.print(
                        "[yellow]" + log["message"] + "[/yellow]", highlight=False
                    )

            self.offset = last_time
            time.sleep(2)

    def stop(self):
        self.stop_flag = True


class _Function:
    """This class is a wrapper around the function to create a function that can be used standalone or as part of a model."""

    print_graph = False
    graph = nx.DiGraph()
    upload = False
    prevent_run = False

    def __init__(
        self,
        function,
        name=None,
        gpu=False,
        python_packages=[],
        python_version=None,
        system_packages=[],
        system_version=None,
        cuda_version=None,
        init_function=None,
        machine_type="",
        iterator_input=False,
        persist_output=False,
        run_commands=[],
        environment_variables: List[Env] = [],
        metadata: Metadata = None,
    ):
        """
        :param function: Function to be wrapped
        :type function: function
        :param name: Name of the function
        :type name: str
        :param gpu: Whether the function needs a GPU
        :type gpu: bool
        :param python_packages: Python packages required by the function
        :type python_packages: list
        :param python_version: Python version required by the function
        :type python_version: str
        :param system_packages: System packages required by the function
        :type system_packages: list
        :param system_version: System version required by the function
        :type system_version: str
        :param cuda_version: CUDA version required by the function
        :type cuda_version: str
        :param init_function: Function to be called when the function is initialized in the event of a setup function for models
        :type init_function: function
        :param machine_type: Machine type required by the function (a100, v100, etc.)
        :type machine_type: str
        :param iterator_input: Whether the function takes an iterator as input
        :type iterator_input: bool
        :param persist_output: Whether the function should persist its output (TODO: remove this)
        :type persist_output: bool
        :param run_commands: Commands to run before the function is called
        :type run_commands: list
        :param environment_variables: Environment variables to set before the function is called
        :type environment_variables: List[Env]
        """

        if function is None:
            self.name = name
            self.remote_function = True
            return

        self.function = function
        self.local_name = function.__name__
        try:
            self.absolute_path = inspect.getfile(function)
        except:
            self.absolute_path = ""
        cwd = os.getcwd()
        self.relative_path = self.absolute_path.replace(cwd, "")
        if self.relative_path[0] == "/":
            self.relative_path = self.relative_path[1:]
        if not name:
            self.name = function.__name__
        self.name = name
        if "/" in self.name or "\\" in self.name or " " in self.name:
            raise InvalidFunctionException(
                f"Function name {self.name} cannot contain '/'"
            )
        self.docstring = None
        if self.function.__doc__:
            self.docstring = docstring_parser.parse(self.function.__doc__)
        self.gpu = gpu
        self.python_packages = python_packages
        self.python_version = python_version
        self.system_packages = system_packages
        self.system_version = system_version
        self.cuda_version = cuda_version
        self.init_function = init_function
        self.machine_type = machine_type
        self.is_iterator_input = iterator_input
        self.persist_output = persist_output
        self.run_commands = run_commands
        self._inputs = get_inputs(self)
        self._check_input_validity()
        self._outputs = get_outputs(self)
        self._output_types = get_output_type(self)
        self.environment_variables = environment_variables
        self.metadata = metadata
        self.node_id = uuid.uuid4().hex
        self.remote_function = False
        self.instance_upload_id = None
        self.id = None
        if init_function and not _Function.print_graph:
            self.init_function()

    def _check_input_validity(self):
        """Check that the function has valid inputs."""
        if len(self._inputs) == 0:
            raise InvalidFunctionException(
                f"Function {self.name} must have at least one input"
            )

    def __setup__(self):
        """Default setup function for functions."""
        pass

    def _has_input_name(self, name):
        """Check if the function has an input with the given name."""

        for inp in self._inputs:
            if inp["name"] == name:
                return True
        return False

    def _get_input_from_name(self, name):
        """Get the input with the given name."""

        for inp in self._inputs:
            if inp["name"] == name:
                return inp
        return None

    def __call__(self, *args, **kwargs):
        """Call the function if not in graph mode."""

        if _Function.print_graph:
            return self._graph(*args, **kwargs)

        if self.remote_function:
            _, name, _ = split_slug(self.name)
            raise RuntimeError(
                f"[red bold]Error:[/red bold] Cannot call a reference function locally. To call a reference function remotely, call {name}.run(*args)."
            )
            return

        current_job = os.environ.get("SIEVE_JOB_ID", "")
        if not current_job:
            print(
                f"[yellow bold]Warning:[/yellow bold] {self.function.__name__} is running on your machine. To run it remotely on Sieve, call {self.function.__name__}.run(*args)."
            )

        return self.function(*args, **kwargs)

    def __get__(self, instance, owner):
        """Get the function if not in graph mode. This is so we can call it."""

        if self.upload:
            return self
        from functools import partial

        return partial(self.__call__, instance)

    def _get_self(self):
        return self

    def _graph(self, *args, **kwargs):
        """
        Call the function in graph mode. This is so we can build the graph for the workflow

        :param args: Arguments to the function
        :type args: list
        :param kwargs: Keyword arguments to the function
        :type kwargs: dict
        :return: Tuple of the node id and output types
        :rtype: Tuple[str, List[Dict[str, str]]]
        """

        for input in self._inputs:
            if hasattr(input, "_name") and input._name == "Iterator":
                self.is_iterator_input = True
        is_iterator_output = inspect.isgeneratorfunction(self.function)
        out = (self.node_id, self._output_types)

        _Function.graph.add_node(
            self.node_id,
            name=self.name,
            type="function",
            inputs=get_input_names(self),
            outputs=get_output_names(self),
            is_iterator_input=self.is_iterator_input,
            is_iterator_output=is_iterator_output,
        )

        for name, (prev_node, param) in kwargs.items():
            if not self._has_input_name(name):
                raise InvalidGraphException(
                    f"Function {self.name} does not have an input named {name}."
                )

            if "type" in self._get_input_from_name(name):
                if param is not inspect._empty and type_to_str(
                    self._get_input_from_name(name)["type"]
                ) != type_to_str(param):
                    raise InvalidGraphException(
                        f"Function {self.name} has an input named {name} with type {self._get_input_from_name(name)['type']} but was passed an input with type {param}."
                    )

            _Function.graph.add_edge(prev_node, self.node_id, input=name)

        input_names = [inp["name"] for inp in self._inputs]
        for item in args:
            if issubclass(type(item), WrappedModelBase):
                # Ignore the surrounding model for model wrapped functions
                continue
            try:
                (prev_node, param) = item
            except:
                raise InvalidFunctionException(
                    f"Function {self.name} has been provided with an invalid input in the workflow {item}. Make sure you only pass in values directly from other functions or the inputs to the workflow."
                )
            try:
                name = input_names.pop(0)
            except:
                raise InvalidFunctionException(
                    f"Function {self.name} has been provided too many inputs in the workflow."
                )

            if "type" in self._get_input_from_name(name):
                if param is not inspect._empty and type_to_str(
                    self._get_input_from_name(name)["type"]
                ) != type_to_str(param):
                    raise InvalidGraphException(
                        f"Function {self.name} has an input named {name} with type {self._get_input_from_name(name)['type']} but was passed an input with type {param}."
                    )

            _Function.graph.add_edge(prev_node, self.node_id, input=name)

        if len(input_names) > 0:
            raise InvalidFunctionException(
                f"Function {self.name} has not been provided all of its inputs in the workflow. Missing inputs: {input_names}"
            )

        return out

    def _graph_validate(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def push(self, *inputs, upload_obj=None, **kwinputs):
        if _Function.prevent_run:
            print(
                f"[yellow bold]Warning:[/yellow bold] Remote function call ({self.name}) prevented to avoid an infinite loop."
            )
            return
        if is_local():
            api_key = get_api_key(None)
        else:
            api_key = get_api_key_no_error(None)
        api_url = os.getenv("SIEVE_API_URL", "https://mango.sievedata.com")
        headers = {}
        if api_key is not None:
            headers["X-API-KEY"] = api_key

        handler = get_global_handler()

        if not self.remote_function:
            if self.instance_upload_id is None:
                # Importing here to avoid circular import
                from ..api.common import upload as upload_function

                model = upload_function(upload_obj or self, single_build=False)
                self.instance_upload_id = model.id
            model_id = self.instance_upload_id or model.id
            stream_output = inspect.isgeneratorfunction(self.function)

        overall_start = time.time()

        pickled_inputs = []
        for input in inputs:
            # Postprocess via handler to upload before sending
            handler.postprocess(input)

            pickled_inputs.append(
                {
                    "name": None,
                    "val": base64.b64encode(cloudpickle.dumps(input)).decode("ascii"),
                }
            )

        for key, value in kwinputs.items():
            # Postprocess via handler to upload before sending
            handler.postprocess(value)

            pickled_inputs.append(
                {
                    "name": key,
                    "val": base64.b64encode(cloudpickle.dumps(value)).decode("ascii"),
                }
            )

        url = f"{api_url}/{V2_API_BASE}/push"
        parent = os.environ.get("SIEVE_JOB_ID", "")
        payload = {
            "inputs": pickled_inputs,
            "serialized": True,
            "parent": parent,
        }
        if self.remote_function:
            payload["function"] = self.name
        else:
            payload["id"] = model_id

        TOTAl_NUM_RETRIES = 5
        for i in range(TOTAl_NUM_RETRIES):
            try:
                response = requests.request("POST", url, headers=headers, json=payload)
                if response.status_code != 200:
                    raise ValueError(f"Could not send job: {response.content}")
                job = response.json()
                if "id" not in job:
                    raise ValueError(f"Could not send job: {response.content}")
                run_id = job["run_id"]
                model_id = job["model_id"]
                stream_output = job["stream_output"]
                break
            except requests.exceptions.SSLError as e:
                # TODO: handle this better, occurs when we push lots of jobs sometimes
                if i == TOTAl_NUM_RETRIES - 1:
                    raise e
                else:
                    time.sleep(0.1)

        stub = create_output_grpc_stub(api_url)
        executor = concurrent.futures.ThreadPoolExecutor()
        TIMEOUT = 60 * 60 * 5  # 5 hours

        def iter_call():
            request = server_pb2.GetOutputsRequest(model_id=model_id, run_id=run_id)
            start_time = time.time()
            while time.time() - start_time < TIMEOUT:
                try:
                    response = stub.GetOutputs(request)
                    for res in response:
                        if res.status == server_pb2.ResponseType.ERROR:
                            raise ValueError(res.error)
                        yield cloudpickle.loads(base64.b64decode(res.value))
                    break
                except grpc.RpcError as e:
                    if (
                        e.code() == grpc.StatusCode.DEADLINE_EXCEEDED
                        or e.code() == grpc.StatusCode.UNAVAILABLE
                        or e.code() == grpc.StatusCode.UNKNOWN
                    ):
                        continue
                    else:
                        raise e
            if time.time() - start_time >= TIMEOUT:
                raise ValueError("Timeout exceeded")

        def single_call():
            request = server_pb2.GetOutputsRequest(model_id=model_id, run_id=run_id)
            start_time = time.time()
            while time.time() - start_time < TIMEOUT:
                try:
                    response = stub.GetOutputs(request)
                    res = next(response)
                except grpc.RpcError as e:
                    if (
                        e.code() == grpc.StatusCode.DEADLINE_EXCEEDED
                        or e.code() == grpc.StatusCode.UNAVAILABLE
                        or e.code() == grpc.StatusCode.UNKNOWN
                    ):
                        continue
                    else:
                        raise e
                break
            if time.time() - start_time >= TIMEOUT:
                raise ValueError("Timeout exceeded")
            if res.status == server_pb2.ResponseType.ERROR:
                raise ValueError(res.error)
            return cloudpickle.loads(base64.b64decode(res.value))

        if stream_output:
            future = executor.submit(iter_call)
        else:
            future = executor.submit(single_call)

        # TODO: return the Job type that acts like a future
        future.job = job
        return future

    def run(self, *inputs, upload_obj=None, **kwinputs):
        if _Function.prevent_run:
            print(
                f"[yellow bold]Warning:[/yellow bold] Remote function call ({self.name}) prevented to avoid an infinite loop."
            )
            return

        future = self.push(*inputs, upload_obj=upload_obj, **kwinputs)
        job = future.job

        if is_local():
            api_key = get_api_key(None)
        else:
            api_key = get_api_key_no_error(None)
        stream_logs_thread = JobLogsThread(api_key, job["id"])
        stream_logs_thread.daemon = True
        stream_logs_thread.start()

        val = future.result()

        stream_logs_thread.stop = True
        return val


class function:
    def __init__(
        self,
        *,
        name=None,
        gpu=False,
        python_packages=[],
        python_version=None,
        system_packages=[],
        system_version=None,
        cuda_version=None,
        machine_type="",
        iterator_input=False,
        persist_output=False,
        run_commands=[],
        environment_variables=[],
        metadata: Metadata = None,
    ):
        self.name = name
        self.gpu = gpu
        self.python_packages = python_packages
        self.python_version = python_version
        self.system_packages = system_packages
        self.system_version = system_version
        self.cuda_version = cuda_version
        self.machine_type = machine_type
        self.iterator_input = iterator_input
        self.persist_output = persist_output
        self.run_commands = run_commands
        self.environment_variables = environment_variables
        self.metadata = metadata

    def __call__(self, function):
        return _Function(
            function,
            name=self.name,
            gpu=self.gpu,
            python_packages=self.python_packages,
            python_version=self.python_version,
            system_packages=self.system_packages,
            system_version=self.system_version,
            cuda_version=self.cuda_version,
            machine_type=self.machine_type,
            iterator_input=self.iterator_input,
            persist_output=self.persist_output,
            run_commands=self.run_commands,
            environment_variables=self.environment_variables,
            metadata=self.metadata,
        )

    @classmethod
    def get(cls, name: str):
        """This method will be called when you use sieve.function.get(...)"""
        if "/" not in name:
            raise InvalidFunctionException(
                f"Function name {name} must be of the format <owner>/<name>"
            )

        return _Function(function=None, name=name)


def split_slug(slug: str):
    owner, version = None, None
    if "/" in slug:
        owner, slug = slug.split("/")
    if ":" in slug:
        slug, version = slug.split(":")
    return owner, slug, version


def get_dict(output):
    """Convert output to a dict."""
    if isinstance(output, list):
        return [get_dict(item) for item in output]
    elif isinstance(output, tuple):
        return tuple([get_dict(item) for item in output])
    elif isinstance(output, dict):
        return output
    elif issubclass(type(output), Struct):
        return output.dict()
    else:
        raise InvalidTypeException(
            "Unknown type",
            type(output),
            "only Struct or subclass or list or tuple is supported",
        )


def from_dict(input, type):
    """Convert input to a type from dict"""
    if hasattr(type, "_name"):
        if type._name == "List":
            return [from_dict(item, type.__args__[0]) for item in input]
        elif type._name == "Dict":
            raise InvalidTypeException("Dict not supported")
        elif type._name == "Tuple":
            return tuple(
                [from_dict(item, type.__args__[i]) for i, item in enumerate(input)]
            )
        elif type._name == "Iterator":
            return from_dict(input, type.__args__[0])
    elif not issubclass(type, Struct):
        raise InvalidTypeException(
            "Unknown type",
            type,
            "only Struct or subclass or list, iterator or tuple is supported",
        )
    else:
        return type.parse_obj(input)


class WrappedModelBase:
    pass


class Model:
    """Decorator to create a model, which is like a function but with a setup and predict function defined."""

    def __init__(
        self,
        name,
        gpu=False,
        python_packages=[],
        python_version=None,
        system_packages=[],
        system_version=None,
        cuda_version=None,
        machine_type="",
        iterator_input=False,
        persist_output=False,
        run_commands=[],
        environment_variables: List[Env] = [],
        metadata: Metadata = None,
    ):
        self.name = name
        self.gpu = gpu
        self.python_packages = python_packages
        self.python_version = python_version
        self.system_packages = system_packages
        self.system_version = system_version
        self.cuda_version = cuda_version
        self.machine_type = machine_type
        self.iterator_input = iterator_input
        self.persist_output = persist_output
        self.run_commands = run_commands
        self.environment_variables = environment_variables
        self.metadata = metadata

    def __setup__(self):
        """Default setup function for models."""
        pass

    def __predict__(self, *args, **kwargs):
        """Default predict function for models."""
        pass

    def __call__(self, cls):
        this = self

        class WrappedModel(WrappedModelBase, cls):
            """
            This class is a wrapper around the model class to create a model that can be used standalone or as part of a workflow. Same definitions as function. Additional specifications below:

            :param absolute_path: Absolute path to the model file
            :type absolute_path: str
            :param relative_path: Relative path to the model file
            :type relative_path: str
            :param source_cls: Source class of the model
            :type source_cls: class
            :param cwd: Current working directory
            :type cwd: str
            :param function: Sieve Function to be wrapped
            :type function: function
            """

            name = this.name
            gpu = this.gpu
            python_packages = this.python_packages
            python_version = this.python_version
            system_packages = this.system_packages
            system_version = this.system_version
            cuda_version = this.cuda_version
            machine_type = this.machine_type
            iterator_input = this.iterator_input
            persist_output = this.persist_output
            run_commands = this.run_commands
            environment_variables = this.environment_variables
            metadata = this.metadata
            try:
                absolute_path = inspect.getfile(cls)
            except:
                absolute_path = "path"
            source_cls = cls
            cwd = os.getcwd()
            relative_path = absolute_path.replace(cwd, "")
            function = function(
                name=this.name,
                gpu=this.gpu,
                python_packages=this.python_packages,
                python_version=this.python_version,
                system_packages=this.system_packages,
                system_version=this.system_version,
                cuda_version=this.cuda_version,
                machine_type=this.machine_type,
                iterator_input=this.iterator_input,
                persist_output=this.persist_output,
                run_commands=this.run_commands,
                environment_variables=this.environment_variables,
                metadata=this.metadata,
            )(
                cls.__predict__,
            )
            this.function = function
            if relative_path[0] == "/":
                relative_path = relative_path[1:]
            if not hasattr(cls, "__predict__"):
                raise InvalidModelException(
                    f"Model {this.name} must have a __predict__ method."
                )

            if not hasattr(cls, "__setup__"):
                raise InvalidModelException(
                    f"Model {this.name} must have a __setup__ method."
                )

            # Throw error if __setup__ has any arguments other than self
            if len(inspect.signature(cls.__setup__).parameters) > 1:
                raise InvalidModelException(
                    f"Model {this.name} __setup__ method can only have self as an argument."
                )

            local_name = cls.__name__

            def __init__(self, *args, **kwargs):
                """Check to see if the model is being initialized in graph mode. Validate setup func."""
                try:
                    super().__init__(*args, **kwargs)
                except TypeError:
                    raise InvalidModelException(
                        f"Model {this.name} __init__/__setup__ methods can only have self as an argument."
                    )
                if not _Function.print_graph:
                    self.__setup__()

            def __call__(self, *args, **kwargs):
                """Call the model if not in graph mode."""
                return self.function(*args, **kwargs)

            def __get__(self, instance, owner):
                """Get the model if not in graph mode. This is so we can call it."""
                from functools import partial

                return partial(self.__call__, instance)

            def run(self, *inputs):
                """Run the model."""
                return this.function.run(*inputs, upload_obj=self)

            def push(self, *inputs):
                """Push the model."""
                return this.function.push(*inputs, upload_obj=self)

            def _get_function():
                """Get the function for calling."""
                return WrappedModel.function

        return WrappedModel

    def __get__(self, instance, owner):
        from functools import partial

        return partial(self.__call__, instance)


def get_inputs(F: _Function) -> List[Dict[str, str]]:
    """
    Validate and return function inputs from the arguments of a Function's function() method.

    :param F: Function to get inputs from
    :type F: Function
    :return: List of inputs
    :rtype: List[Dict[str, str]]
    """

    signature = inspect.signature(F.function)

    # Get all the input arg names and types
    inputs = []
    for name, parameter in signature.parameters.items():
        if name == "self":
            continue
        inp = {"name": name}

        # Omit type if not provided by user
        if parameter.annotation is not inspect._empty:
            inp["type"] = parameter.annotation
            inp["schema"] = type_to_schema(inp["type"])
        inputs.append(inp)

    if F.docstring:
        params = F.docstring.params
        params_map = {}
        for param in params:
            params_map[param.arg_name] = param.description

        for input in inputs:
            if input["name"] in params_map:
                input["description"] = params_map[input["name"]]

    return inputs


def get_input_names(F: _Function) -> List[Dict[str, str]]:
    """
    Validate and return function input names from the arguments of a Function's function() method.

    :param F: Function to get input names from
    :type F: Function
    :return: List of input names
    :rtype: List[Dict[str, str]]
    """

    signature = inspect.signature(F.function)

    # Get all the input arg names and types
    inputs = []
    for name, parameter in signature.parameters.items():
        if name == "self":
            continue
        inp = {"name": name}

        # Omit type if not provided by user
        if parameter.annotation is not inspect._empty:
            inp["type"] = type_to_str(parameter.annotation)
            inp["schema"] = type_to_schema(parameter.annotation)
        # If a default arg is specified, add a field["data"] with the base64 encoded cloud pickle dump of the default arg
        if parameter.default is not inspect._empty:
            inp["data"] = base64.b64encode(cloudpickle.dumps(parameter.default)).decode(
                "utf-8"
            )
        inputs.append(inp)

    if F.docstring:
        params = F.docstring.params
        params_map = {}
        for param in params:
            params_map[param.arg_name] = param.description

        for input in inputs:
            if input["name"] in params_map:
                input["description"] = params_map[input["name"]]

    return inputs


def get_outputs(F: _Function) -> List[Dict[str, str]]:
    """
    Validate and return function outputs from the return type of a Function's function() method.

    :param F: Function to get outputs from
    :type F: Function
    :return: List of outputs
    :rtype: List[Dict[str, str]]
    """
    signature = inspect.signature(F.function)

    # TODO: start supporting multiple outputs for functions
    if signature.return_annotation is not inspect._empty:
        return [{"type": signature.return_annotation}]
    return [{}]


def get_output_names(F: _Function) -> List[Dict[str, str]]:
    """
    Validate and return function output names from the return type of a Function's function() method.

    :param F: Function to get output names from
    :type F: Function
    :return: List of output names
    :rtype: List[Dict[str, str]]
    """

    signature = inspect.signature(F.function)

    description = None
    if F.docstring and F.docstring.returns:
        description = F.docstring.returns.description

    # TODO: start supporting multiple outputs for functions
    if signature.return_annotation is not inspect._empty:
        return [
            {
                "type": type_to_str(signature.return_annotation),
                "description": description,
            }
        ]

    return [{"description": description}]


def get_output_type(F: _Function):
    """Validate and return function output type from the return type of a Function's function() method."""

    signature = inspect.signature(F.function)
    return signature.return_annotation


def unwrap_type(type_):
    """Unwrap a type from a type hint."""
    if hasattr(type_, "_name") and (
        type_._name == "Iterator"
        or type_._name == "Iterable"
        or type_._name == "List"
        or type_._name == "Tuple"
    ):
        return type_.__args__[0]
    else:
        return type_


def create_output_grpc_stub(api_url):
    api_host = api_url.split("//")[1]
    options = [("grpc.keepalive_time_ms", 10000)]

    if api_url.startswith("https://"):
        credentials = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(f"{api_host}:443", credentials, options=options)
    else:
        channel = grpc.insecure_channel(f"{api_host}:80", options=options)
    stub = server_pb2_grpc.OutputServiceStub(channel)
    return stub
