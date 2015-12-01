#!/usr/bin/env bash

project_root=

function find_script_path() {
    PROG_PATH=${BASH_SOURCE[0]}
    PROG_NAME=${PROG_PATH##*/}
    PROG_DIR=$(cd "$(dirname "${PROG_PATH:-$PWD}")" 2>/dev/null 1>&2 && pwd)
    project_root=${PROG_DIR}/..
}

find_script_path
cd ${project_root}
# lint and pep8 check
echo "flake8"
flake8
#
echo "coverage run --source=pages ./setup.py test"
coverage run --source=pages ./setup.py test
#
echo "coverage html"
coverage html
