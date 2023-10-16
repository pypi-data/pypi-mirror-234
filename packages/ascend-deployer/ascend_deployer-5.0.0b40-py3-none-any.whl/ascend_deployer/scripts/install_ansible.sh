#!/bin/bash
readonly BASE_DIR_ANSIBLE=$(
    cd "$(dirname $0)" >/dev/null 2>&1
    pwd -P
)

readonly PYLIB_PATH_ANSIBLE=${BASE_DIR_ANSIBLE}/../resources/pylibs
function get_specified_python() {
    if [ ! -z ${ASCEND_PYTHON_VERSION} ]; then
        echo ${ASCEND_PYTHON_VERSION}
    else
        echo $(grep -oP "^ascend_python_version=\K.*" ${BASE_DIR_ANSIBLE}/../downloader/config.ini | sed 's/\r$//')
    fi
}
readonly specified_python_ansible=$(get_specified_python)

readonly PYTHON_VERSION_ANSIBLE=$(echo ${specified_python_ansible} | sed 's/P/p/;s/-//')

readonly PYTHON_MINOR_ANSIBLE=$(echo ${PYTHON_VERSION_ANSIBLE%.*})

readonly PYTHON_PREFIX_ANSIBLE=${HOME}/.local/${PYTHON_VERSION_ANSIBLE}

function install_ansible() {
    echo "install ansible"
    local ansible_path=${PYTHON_PREFIX_ANSIBLE}/lib/${PYTHON_MINOR_ANSIBLE}/site-packages/ansible
    ${PYTHON_MINOR_ANSIBLE} -m ensurepip
    ${PYTHON_MINOR_ANSIBLE} -m pip install --upgrade pip --no-index --find-links ${PYLIB_PATH_ANSIBLE}
    ${PYTHON_MINOR_ANSIBLE} -m pip install ansible-core --no-index --find-links ${PYLIB_PATH_ANSIBLE}
    # patch the INTERPRETER_PYTHON_DISTRO_MAP, make it support EulerOS
    if [ -f ${ansible_path}/config/base.yml ]; then
        eulercnt=$(grep euleros ${ansible_path}/config/base.yml | wc -l)
        if [ ${eulercnt} == 0 ]; then
            # euler os 2 is recoginized as centos 2
            sed -i "1501 i\      '2': /usr/bin/python3" ${ansible_path}/config/base.yml
            # ubuntu 18.04 is recoginized as debian buster/sid due tu /etc/debian_release
            sed -i "1506 i\      'buster/sid': /usr/bin/python3" ${ansible_path}/config/base.yml
            # euler os use python3 as default python interpreter
            sed -i "1516 i\    euleros:" ${ansible_path}/config/base.yml
            sed -i "1517 i\      '2': /usr/bin/python3" ${ansible_path}/config/base.yml
            # kylin should use python3. if selinux enalbed, the default python have no selinux
            sed -i "1518 i\    kylin:" ${ansible_path}/config/base.yml
            sed -i "1519 i\      '10': /usr/bin/python3" ${ansible_path}/config/base.yml
            sed -i "1520 i\      'V10': /usr/bin/python3" ${ansible_path}/config/base.yml
            # debian 10.0
            sed -i "1506 i\      '10.0': /usr/bin/python3" ${ansible_path}/config/base.yml
            # ubuntu 20.04 is recoginized as debian bullseye/sid due to /etc/debian_version
            sed -i "1508 i\      'bullseye/sid': /usr/bin/python3" ${ansible_path}/config/base.yml
            # openeuler os use python3 as default python interpreter
            sed -i "1523 i\    openeuler:" ${ansible_path}/config/base.yml
            sed -i "1524 i\      '20.03': /usr/bin/python3" ${ansible_path}/config/base.yml
            sed -i "1525 i\    uos:" ${ansible_path}/config/base.yml
            sed -i "1526 i\      '20': /usr/bin/python3" ${ansible_path}/config/base.yml
            sed -i "1527 i\    uniontech:" ${ansible_path}/config/base.yml
            sed -i "1528 i\      '20': /usr/bin/python3" ${ansible_path}/config/base.yml
        fi
    fi
}


function checkAnsible() {
    ansible --version >/dev/null 2>&1
    echo $?
}

function check_and_install_ansible() {
    local is_ansible_installed=$(checkAnsible)
    if [[ ${is_ansible_installed} != 0 ]];then
        if [ ! -d ${BASE_DIR_ANSIBLE}/../resources ];then
            echo -e "[ERROR]\t$(date +"%Y-%m-%d %H:%M:%S")\t error: no resource dir"
            exit 1
        else
            install_ansible
        fi
    fi
}

check_and_install_ansible
