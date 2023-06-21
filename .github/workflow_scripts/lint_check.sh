#!/bin/bash

set -ex

source $(dirname "$0")/env_setup.sh

setup_lint_env

black --check --diff app/ scripts/ plotting/ tests/
isort --profile black --check --diff app/ scripts/ plotting/ tests/ 