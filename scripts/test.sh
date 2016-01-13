#!/usr/bin/env bash

project_root=

function find_script_path() {
    PROG_PATH=${BASH_SOURCE[0]}
    PROG_NAME=${PROG_PATH##*/}
    PROG_DIR=$(cd "$(dirname "${PROG_PATH:-$PWD}")" 2>/dev/null 1>&2 && pwd)
    project_root=${PROG_DIR}/..
}

function check_outcome() {
    if [ "$?" != "0" ]; then
        echo $1
        exit 1
    fi
}

find_script_path
cd ${project_root}

pip install --upgrade pip

echo "installing requirements"
pip install -r ./requirements/requirements.txt --upgrade
pip install -r ./requirements/requirements-ci.txt --upgrade

# lint and pep8 check
echo "running flake8"
flake8
check_outcome "flake8 failure. quitting."

# unit test + coverage
echo "coverage run --source=pages ./setup.py test"
coverage run --source=pages ./setup.py test

check_outcome "tests failed. quitting."

# genrating html report
echo "coverage html"
coverage html
