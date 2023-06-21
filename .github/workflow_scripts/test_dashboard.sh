#!/bin/bash
set -ex

python3 -m pytest --junitxml=results.xml unittests/