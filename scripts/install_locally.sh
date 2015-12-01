#!/bin/sh -x

project_root=
lib_name=uitestcommons

function find_script_path() {
    PROG_PATH=${BASH_SOURCE[0]}
    PROG_NAME=${PROG_PATH##*/}
    PROG_DIR=$(cd "$(dirname "${PROG_PATH:-$PWD}")" 2>/dev/null 1>&2 && pwd)
    project_root=${PROG_DIR}/..
}

find_script_path

# remove dist folder if any
if [ -a ${project_root}/build ]; then
    rm -rf "${project_root}/build"
fi
if [ -a ${project_root}/dist ]; then
    rm -rf "${project_root}/dist"
fi
if [ -a ${project_root}/testcommons.egg-info ]; then
    rm -rf "${project_root}/${lib_name}.egg-info"
fi

# generate wheel
python setup.py bdist_wheel

# install wheel
wheel_name=$(pip freeze | grep ${lib_name})
cd ${project_root}/dist
if [ -z "${wheel_name}" ]; then
    pip install ${lib_name} --find-links=.
else
    pip uninstall ${lib_name}
    pip install ${lib_name} --find-links=.
fi
