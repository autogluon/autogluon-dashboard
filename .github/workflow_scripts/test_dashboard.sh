#!/bin/bash
set -ex

source $(dirname "$0")/env_setup.sh

install_dashboard_test

python3 -m pytest --junitxml=results.xml tests/unittests/ --ignore=tests/unittests/coverage/ --cov-report json
