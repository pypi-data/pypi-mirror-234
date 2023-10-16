
PROJECT_OWNER := AccidentallyTheCable
PROJECT_EMAIL := cableninja@cableninja.net
PROJECT_FIRST_YEAR := 2023
PROJECT_LICENSE := GPLv3
PROJECT_NAME := atckit
PROJECT_DESCRIPTION := AccidentallyTheCables Utility Kit
PROJECT_VERSION := $(shell egrep "^version =" pyproject.toml | awk '{print $$3}' | tr -d '"')

## Enable Feature 'Python'
BUILD_PYTHON := 1
## Enable Feature 'Shell'
BUILD_SHELL := 0
## Enable python `dist` Phase for Projects destined for PYPI
PYTHON_PYPI_PROJECT := 1
## Additional Flags for pylint. EX --ignore-paths=mypath
PYLINT_EXTRA_FLAGS := 

### Any Further Project-specific make targets can go here

project_extra_build_deps:  ## Install `build_requirements.txt
	python3 -m pip install -r ${THIS_DIR}/build_requirements.txt
