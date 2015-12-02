#!/usr/bin/env bash

echo "Preparing for distributing pages"

project_root=

function find_script_path() {
    PROG_PATH=${BASH_SOURCE[0]}
    PROG_NAME=${PROG_PATH##*/}
    PROG_DIR=$(cd "$(dirname "${PROG_PATH:-$PWD}")" 2>/dev/null 1>&2 && pwd)
    project_root=${PROG_DIR}/..
}

find_script_path
cd ${project_root}

if [ -d "build" ]; then
    rm -rf build
fi

if [ -d "dist" ]; then
    rm -rf dist
fi

if [ -d "pages.egg-info" ]; then
    rm -rf pages.egg-info
fi

pip install --upgrade pip

echo "installing requirements"
pip install -r ./requirements/requirements-dist.txt --upgrade

echo "running tests"
./scripts/test.sh

if [ "$?" != "0" ]; then
    exit 1
fi


if [ "$1" == "--no-upload" ]
then
    echo "creating source distribution"
    python ./setup.py sdist
    echo "creating wheel distribution"
    python ./setup.py bdist_wheel
else
    echo "uploading source distribution"
    python ./setup.py sdist upload -r pypi

    echo "uploading wheel distribution"
    python ./setup.py bdist_wheel upload -r pypi
fi
