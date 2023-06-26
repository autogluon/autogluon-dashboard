#!/bin/bash

set -ex

source $(dirname "$0")/env_setup.sh

setup_lint_env

black --check --diff src/ tests/ --extend-exclude tests/unittests/out_file
isort --profile black --check --diff src/ tests/ --skip-glob tests/unittests/out_file
