#!/bin/bash
set -ex

source $(dirname "$0")/env_setup.sh

install_dashboard_test

python3 -m pytest --junitxml=results.xml tests/unittests/ --cov-report json:tests/unittests/coverage/coverage.json
