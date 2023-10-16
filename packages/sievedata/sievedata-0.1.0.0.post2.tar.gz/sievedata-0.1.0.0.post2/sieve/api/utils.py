"""
Utility functions for the Sieve API
"""

import requests

import os

import os
import shutil
import zipfile


def parse_gitignore(gitignore_path):
    """Parse the .gitignore file and return a list of patterns to ignore."""

    ignore_patterns = []
    with open(gitignore_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            ignore_patterns.append(line)
    return ignore_patterns


def zip_directory(directory_path, zip_filename):
    """Zip a directory and return the zip file path"""

    temp_directory = os.path.join(os.path.dirname(directory_path), "__temp__")

    # Remove files and directories mentioned in .gitignore
    gitignore_path = os.path.join(directory_path, ".gitignore")
    ignore_patterns = [".git/*", ".git"]
    if os.path.exists(gitignore_path):
        ignore_patterns.extend(parse_gitignore(gitignore_path))

    shutil.copytree(
        directory_path, temp_directory, ignore=shutil.ignore_patterns(*ignore_patterns)
    )

    # Create the zip file
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_directory)
                zipf.write(file_path, arcname)

    # Clean up the temporary directory
    shutil.rmtree(temp_directory, ignore_errors=True)

    return zip_filename


def get_config_file_path():
    """
    Get the config file path
    """
    config_file_path = os.path.join(
        os.path.expanduser("~"), ".config", ".sieve", "config"
    )
    return config_file_path


def read_config_file():
    """
    Read the config file
    """
    path = get_config_file_path()
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return f.read()


def get_api_key(API_KEY):
    """Get the API key from the environment variable or from the argument"""
    if API_KEY is not None:
        api_key = API_KEY
    else:
        api_key = os.environ.get("SIEVE_API_KEY")
        if api_key is None:
            api_key = read_config_file()
        if not api_key:
            raise ValueError(
                "Please set environment variable SIEVE_API_KEY with your API key"
            )
    return api_key


def get_api_key_no_error(API_KEY):
    """Get the API key from the environment variable or from the argument"""
    if API_KEY is not None:
        api_key = API_KEY
    else:
        api_key = read_config_file()
        if api_key is None:
            api_key = os.environ.get("SIEVE_API_KEY")
    return api_key
