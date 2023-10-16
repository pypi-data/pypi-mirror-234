# Lectric Software Development Kit (SDK)

Programmatic access to the lectric vector database service.

## Installation

The SDK is exposed as a simple python package. There are two main ways it can be installed.

## Developers

Clone the git repo and install from source:

First clone the repo from [here](https://dev.azure.com/msresearch/WatchFor/_git/lectric), then
```
cd lectric/client
python -m pip install -U -r requirements-dev.txt
python setup.py install
```

### Generating the client

`pipx install openapi-python-client --include-deps`.


* Then replace the source files with the `w4-dev` branch of [https://pkgs.dev.azure.com/watchfor/WatchForTools/_packaging/w4Tools/pypi/simple/](https://pkgs.dev.azure.com/watchfor/WatchForTools/_packaging/w4Tools/pypi/simple/)

This will create the `openapi-python-client.exe` executable.

### Running the tests

In order to run the client (SDK) tests a server running on `http://localhost:8000`, with an appropriate `lectric_config.yaml` exported as
an environment variable.

```
cd tests
python -m pytest -s .
```


### Modifying the SDK

The main wrapper to the auto-generated client is located within `lectric/lectric_client.py`.
To refresh/recreate the auto-generated client library. Make sure to run the `uvicorn` fastapi sever from at port `8000`:
```
uvicorn main:app --reload
```

,then generate the client.

```
./generate.sh
```

## General Users

We highly recommend installing Lectric within a virtual environment to avoid package
versioning mismatches. For `Python 3.6+`

### Mac/Linux

```
python -m venv lectric-env
source lectric-env/Scripts/activate
```

### Windows

```
python -m venv lectric-env
./lectric-env/Scripts/Activate.ps1
```


Then install from our WatchFor PyPI registry as follows:

```
pip install --index-url https://pkgs.dev.azure.com/watchfor/WatchForTools/_packaging/w4Tools/pypi/simple/ watchfor-lectric-sdk==<VERSION>
```

Where `<VERSION>` is your desired version (at the time of edit `0.0.3`).


## Checking Installation

Simply run:

```
import lectric
print(lectric.version()) # Should return a string with the version you installed
```

## Documentation

HTML docs are maintained within `docs/build/html`. To review docs open `index.html` within any browser.

## Building the docs

Install the sphinx on the system as per the instructions [here](https://www.sphinx-doc.org/en/master/usage/installation.html).
A few examples are:
**Windows**: `choco install sphinx`
**Ubuntu**: `apt-get install python3-sphinx`
This should put `sphinx-build` on the path.

Then within `docs` run `make html`, for html docs.
