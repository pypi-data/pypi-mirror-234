"""
This module describes how we handle files and arrays in Sieve using our specialized types.
"""

import sieve
import random
import requests
import tempfile
import time
import hashlib
from typing import Any, Dict
import os
from pydantic import BaseModel
from sieve.api.constants import API_URL, API_BASE, V2_API_BASE
import uuid
from sieve.api.utils import get_api_key

from ..logging.logging import get_sieve_internal_logger

logger = get_sieve_internal_logger()

FILESERVER_ID = "fileserver_sha256"
FILE_SUFFIX = "file_suffix"

global_handler = None


def get_global_handler():
    global global_handler
    if global_handler is None:
        global_handler = Handler()
    return global_handler


class Handler:
    """
    This class handles file server interaction to pre and postprocess inputs and outputs.

    It is responsible for downloading and uploading files and arrays to the file server,
    which is passed in dynamically. For Sieve types, it creates an internal dictionary
    to store the file server hash. It also stores a set of hashes to prevent duplicate
    uploads. We also make it fault tolerant in case of connection errors.
    """

    def __init__(self):
        self.file_hashes = set()
        self.file_server_url = ""
        self.file_server_headers = {}

    def set_file_server_url(self, url: str):
        self.file_server_url = url

    def set_file_server_headers(self, headers: Dict[str, str]):
        self.file_server_headers = headers

    def preprocess(self, prediction_input: Any):
        if isinstance(prediction_input, list):
            [self.preprocess(x) for x in prediction_input]
            return
        elif isinstance(prediction_input, tuple):
            [self.preprocess(x) for x in prediction_input]
            return
        if issubclass(type(prediction_input), sieve.Array):
            self.download_array(prediction_input)
        elif issubclass(type(prediction_input), sieve.File):
            self.download_file(prediction_input)
        elif issubclass(type(prediction_input), BaseModel):
            [self.preprocess(x) for x in prediction_input.__dict__.values()]

    def postprocess(self, prediction_output: Any):
        if isinstance(prediction_output, list):
            [self.postprocess(x) for x in prediction_output]
            return
        elif isinstance(prediction_output, tuple):
            [self.postprocess(x) for x in prediction_output]
            return
        if issubclass(type(prediction_output), sieve.Struct):
            self.create_internal(prediction_output)
        if issubclass(type(prediction_output), sieve.Array):
            self.upload_array(prediction_output)
        elif issubclass(type(prediction_output), sieve.File):
            self.upload_file(prediction_output)
        elif issubclass(type(prediction_output), BaseModel):
            [self.postprocess(x) for x in prediction_output.__dict__.values()]

    def create_internal(self, struct: sieve.Struct):
        if hasattr(struct, "_internal"):
            logger.info(
                f"sieve struct {struct} already has attribute _internal, not creating"
            )
            return
        for name, value in struct.__dict__.items():
            if issubclass(type(value), sieve.Struct):
                self.create_internal(value)
        struct._internal = {}

    def is_local(self):
        return self.file_server_url == ""

    def upload_file(self, file: sieve.File):
        if not self.is_local():
            self.upload_file_to_server(file)
        else:
            self.upload_file_to_sieve(file)

    def upload_array(self, image: sieve.Image):
        if not self.is_local():
            self.upload_array_to_server(image)
        else:
            self.upload_array_to_sieve(image)

    def download_array(self, array: sieve.Array):
        if self.is_local():
            return
        self.download_array_from_server(array)

    def download_file(self, file: sieve.File):
        if self.is_local():
            return
        self.download_file_from_server(file)

    def download_array_from_server(self, array: sieve.Array):
        if not hasattr(array, "_internal") or array._internal is None:
            logger.info("sieve array has no attribute _internal")
            return
        if array._internal.get(FILESERVER_ID) is None:
            logger.info("sieve array internal has no hash")
            return
        file_server_url = (
            self.file_server_url + "/" + array._internal.get(FILESERVER_ID)
        )
        try:
            r = file_server_get_exponential_backoff(
                file_server_url, headers=self.file_server_headers
            )
        except requests.exceptions.ChunkedEncodingError as e:
            raise Exception(
                "Failed to download file from file server at URL: "
                + file_server_url
                + " with error: "
                + str(e)
            )

        if r.status_code != 200:
            logger.info(f"Failed to download file from file server {r.text}")
        array._data = r.content
        self.file_hashes.add(array._internal.get(FILESERVER_ID))

    def download_file_from_server(self, file: sieve.File):
        if not hasattr(file, "_internal") or file._internal is None:
            logger.info("sieve file has no attribute _internal")
            return
        if file._internal.get(FILESERVER_ID) is None:
            logger.info("sieve file internal has no hash")
            return
        # Stream potentially large files
        r = file_server_get_exponential_backoff(
            self.file_server_url + "/" + file._internal.get(FILESERVER_ID),
            headers=self.file_server_headers,
            stream=True,
        )
        suffix = file._internal.get(FILE_SUFFIX)
        if suffix is not None:
            suffix = "." + suffix
        if r.status_code != 200:
            logger.info(f"Failed to download file from file server {r.text}")
        _, local_filename = tempfile.mkstemp(
            dir="/mountedssd" if os.path.exists("/mountedssd") else None, suffix=suffix
        )
        file._path = local_filename
        with open(file._path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        self.file_hashes.add(file._internal.get(FILESERVER_ID))

    def upload_file_to_server(self, file: sieve.File):
        # Upload file to GCP
        if file._path is None:
            return
        hash = hashlib.sha256()
        BUF_SIZE = 262144
        with open(file._path, "rb") as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                hash.update(data)
        file._internal[FILESERVER_ID] = hash.hexdigest()

        if file._internal[FILESERVER_ID] in self.file_hashes:
            file._path = None
            return
        with open(file._path, "rb") as f:
            file_suffix = file._path.split(".")[-1]
            r = file_server_put_exponential_backoff(
                self.file_server_url + "/", data=f, headers=self.file_server_headers
            )
            if r.status_code != 200:
                raise Exception("Failed to upload file to file server")
            file._internal[FILESERVER_ID] = r.text
            file._internal[FILE_SUFFIX] = file_suffix
        file._path = None
        self.file_hashes.add(file._internal[FILESERVER_ID])

    def upload_file_to_sieve(self, file: sieve.File):
        if file._path is None:
            return
        file_suffix = file._path.split(".")[-1]

        api_key = get_api_key()
        if not api_key:
            raise Exception(
                "SIEVE_API_KEY environment variable not set, must be set to upload files to Sieve"
            )

        upload_url_url = f"{API_URL}/{API_BASE}/upload_url"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
        }
        payload = {"file_name": str(uuid.uuid4()) + "." + file_suffix}

        upload_response = requests.request(
            "POST", upload_url_url, headers=headers, json=payload
        )

        upload_url_json = upload_response.json()
        upload_url = upload_url_json["upload_url"]
        headers = {"x-goog-content-length-range": "0,10000000000"}
        file_upload_response = requests.request(
            "PUT", upload_url, headers=headers, data=open(file._path, "rb")
        )
        if file_upload_response.status_code != 200:
            raise Exception("Failed to upload file to Sieve")
        file._path = None
        file.url = upload_url_json["get_url"]

    def upload_array_to_server(self, sieve_array: sieve.Array):
        # convert sieve_array.data string to bytes
        if sieve_array._data is None:
            if sieve_array._path is not None:
                return self.upload_file_to_server(sieve_array)
        d = sieve_array.data
        if d is None:
            return

        hash = hashlib.sha256(d)
        sieve_array._internal[FILESERVER_ID] = hash.hexdigest()
        if sieve_array._internal[FILESERVER_ID] in self.file_hashes:
            sieve_array._data = None
            return
        r = file_server_put_exponential_backoff(
            self.file_server_url + "/",
            data=sieve_array.data,
            headers=self.file_server_headers,
        )
        if not (200 <= r.status_code < 300):
            sieve_array._data = None
            raise Exception("Failed to upload string to file server", r.text)
        sieve_array._internal[FILESERVER_ID] = r.text
        sieve_array._data = None
        sieve_array._array = None
        self.file_hashes.add(sieve_array._internal[FILESERVER_ID])

    def upload_array_to_sieve(self, sieve_array: sieve.Array):
        # convert sieve_array.data string to bytes
        if sieve_array._data is None:
            if sieve_array._path is not None:
                return self.upload_file_to_sieve(sieve_array)
        d = sieve_array.data
        if d is None:
            return

        api_key = get_api_key()
        if not api_key:
            raise Exception(
                "SIEVE_API_KEY environment variable not set, must be set to upload files to Sieve"
            )

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
            "PUT", upload_url, headers=headers, data=d
        )
        if file_upload_response.status_code != 200:
            raise Exception("Failed to upload file to Sieve")
        sieve_array._data = None
        sieve_array.url = upload_url_json["get_url"]


def file_server_put_exponential_backoff(url, data, headers=None):
    retry_delay = 0.05
    for i in range(10):
        if i > 0:
            time.sleep(retry_delay * random.uniform(1, 2))
            retry_delay *= 2
        try:
            r = requests.put(url, data, headers=headers)
            if 200 <= r.status_code < 300:
                return r
        except requests.exceptions.ConnectionError as e:
            logger.info("Connection error: " + str(e))
        data.seek(0)
    return r


def file_server_get_exponential_backoff(url, headers=None, stream=None):
    retry_delay = 0.05
    for i in range(10):
        if i > 0:
            time.sleep(retry_delay * random.uniform(1, 2))
            retry_delay *= 2
        try:
            r = requests.get(url, headers=headers, stream=stream)
            if 200 <= r.status_code < 300:
                return r
        except requests.exceptions.ConnectionError as e:
            logger.info("Connection error: " + str(e))
    return r
