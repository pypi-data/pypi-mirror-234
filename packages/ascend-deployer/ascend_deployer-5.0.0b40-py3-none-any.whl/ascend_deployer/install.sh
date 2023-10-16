#!/bin/bash
readonly BASE_DIR=$(
    cd "$(dirname $0)" >/dev/null 2>&1
    pwd -P
)

function get_specified_python() {
    if [ ! -z ${ASCEND_PYTHON_VERSION} ]; then
        echo ${ASCEND_PYTHON_VERSION}
    else
        echo $(grep -oP "^ascend_python_version=\K.*" ${BASE_DIR}/downloader/config.ini | sed 's/\r$//')
    fi
}

readonly specified_python=$(get_specified_python)
readonly PYTHON_VERSION=$(echo ${specified_python} | sed 's/P/p/;s/-//')
readonly PYTHON_PREFIX=${HOME}/.local/${PYTHON_VERSION}
export PATH=${PYTHON_PREFIX}/bin:$PATH
export LD_LIBRARY_PATH=${PYTHON_PREFIX}/lib:$LD_LIBRARY_PATH


main() {
    python3 -V > /dev/null 2>&1
    if [[ $? != 0 ]]; then
      python ${BASE_DIR}/ascend_deployer.py $*
    else
      python3 ${BASE_DIR}/ascend_deployer.py $*
    fi
}

main $*
main_status=$?
exit ${main_status}
