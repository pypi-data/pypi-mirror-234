from setuptools import setup, find_packages

VERSION = "0.1.0.0-2"

f = open("README.md", "r")
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name="sievedata",
    version=VERSION,
    description="Sieve CLI and Python Client",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Sieve Team",
    author_email="developer@sievedata.com",
    url="https://github.com/sieve-data/sieve",
    license="unlicensed",
    packages=find_packages(exclude=["ez_setup", "tests*"]),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.0",
        "click>=8.0",
        "pydantic==1.10.9",
        "pathlib>=1.0.1",
        "typing>=3.6",
        "numpy>=1.19.0",
        "argparse>=1.4.0",
        "tqdm==4.64.1",
        "uuid>=1.30",
        "networkx",
        "opencv-python-headless==4.5.5.64",
        "typeguard",
        "pillow",
        "typer>=0.7.0",
        "rich",
        "cloudpickle",
        "docstring_parser",
        "jsonref",
        "protobuf==3.20.3",
        "pyyaml",
        "grpcio==1.54.0",
        "sseclient",
    ],
    entry_points={
        "console_scripts": [
            "sieve = cli.sieve:cli",
        ]
    },
)
