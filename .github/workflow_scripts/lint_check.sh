#!/bin/bash

set -ex

source $(dirname "$0")/env_setup.sh

setup_lint_env

black --check --diff src/ tests/
isort --profile black --check --diff src/ tests/ 