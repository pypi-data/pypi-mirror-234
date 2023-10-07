# Portal Pipeline Utilities

Utilities for deploying pipelines and interfacing with portal infrastructure.

For more information on available commands and how to contribute and deploy pipelines within the infrastructure check the extended [*documentation*](https://portal-pipeline-utils.readthedocs.io/en/latest/ "portal-pipeline-utils documentation").

## Install

The software is python based. To install the software and the required packages, we recommend using a fresh virtual environment.
Please refer to `pyproject.toml` for the supported Python versions.

The package is available on [*pypi*](https://pypi.org/project/portal-pipeline-utils "portal-pipeline-utils pypi"):

    pip install portal-pipeline-utils

To install from source:

    git clone https://github.com/dbmi-bgm/portal-pipeline-utils.git
    cd portal-pipeline-utils
    make configure
    make update
    make build

To check that the software is correctly installed, try to run `pipeline_utils`. If installed from source, this command may fail with a bash “command not found” error, try `poetry run pipeline_utils` instead.

See `make info` for details on make targets.
