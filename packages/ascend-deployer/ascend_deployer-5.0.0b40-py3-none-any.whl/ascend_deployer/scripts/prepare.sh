#!/bin/bash
readonly TRUE=1
readonly FALSE=0
readonly kernel_version=$(uname -r)
readonly arch=$(uname -m)
readonly BASE_DIR=$(
    cd "$(dirname $0)/.." >/dev/null 2>&1
    pwd -P
)
readonly PYLIB_PATH=${BASE_DIR}/resources/pylibs

declare -A OS_MAP=(["ubuntu"]="Ubuntu")
OS_MAP["ubuntu"]="Ubuntu"
OS_MAP["centos"]="CentOS"
OS_MAP["euleros"]="EulerOS"
OS_MAP["debian"]="Debian"
OS_MAP["kylin"]="Kylin"
OS_MAP["bclinux"]="BCLinux"
OS_MAP["Linx"]="Linx"
OS_MAP["UOS"]="UOS"
OS_MAP["uos"]="UOS"
OS_MAP["tlinux"]="Tlinux"
OS_MAP["openEuler"]="OpenEuler"
OS_MAP["ctyunos"]="CTyunOS"

function log_info() {
    local DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N=$(whoami)
    local IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "[INFO] $*"
    echo "${DATE_N} ${USER_N}@${IP_N} [INFO] $*" >>${BASE_DIR}/install.log
}

function log_warning() {
    local DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N=$(whoami)
    local IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "[WARNING] $*"
    echo "${DATE_N} ${USER_N}@${IP_N} [WARNING] $*" >>${BASE_DIR}/install.log
}

function log_error() {
    local DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N=$(whoami)
    local IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "[ERROR] $*"
    echo "${DATE_N} ${USER_N}@${IP_N} [ERROR] $*" >>${BASE_DIR}/install.log
}

function operation_log_info() {
    local DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N=$(whoami)
    local IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "${DATE_N} ${USER_N}@${IP_N} [INFO] $*" >>${BASE_DIR}/install_operation.log
}

function get_specified_python() {
    if [ ! -z ${ASCEND_PYTHON_VERSION} ]; then
        echo ${ASCEND_PYTHON_VERSION}
    else
        echo $(grep -oP "^ascend_python_version=\K.*" ${BASE_DIR}/downloader/config.ini | sed 's/\r$//')
    fi
}

readonly specified_python=$(get_specified_python)

function check_python_version() {
    if $(echo "${specified_python}" | grep -Evq '^Python-3.(7|8|9).([0-9]|1[0-1])$'); then
        log_error "ascend_python_version is not available, available Python-x.x.x is in 3.7.0~3.7.11 and 3.8.0~3.8.11 and 3.9.0~3.9.9"
        return 1
    fi
}

readonly PYTHON_TAR=${specified_python}
readonly PYTHON_VERSION=$(echo ${specified_python} | sed 's/P/p/;s/-//')
readonly PYTHON_MINOR=$(echo ${PYTHON_VERSION%.*})
readonly PYTHON_PREFIX=${HOME}/.local/${PYTHON_VERSION}
export PATH=${PYTHON_PREFIX}/bin:$PATH
export LD_LIBRARY_PATH=${PYTHON_PREFIX}/lib:$LD_LIBRARY_PATH

function get_os_version() {
    local id=${1}
    local ver=${2}
    local codename=${3}
    local version=${ver}

    # Ubuntu
    if [ "${id}" == "Ubuntu" ]; then
        ubuntu_version=$(grep -oP "^PRETTY_NAME=\K.*" /etc/os-release|awk '{print $2}')
        if [[ $ubuntu_version =~ 18.04 ]] && [[ $ubuntu_version != 18.04.1 ]] && [[ $ubuntu_version != 18.04.5 ]];then
            version=$ubuntu_version
        fi
    fi

    # CentOS
    if [ "${id}" == "CentOS" ]; then
        version=$(cat /etc/centos-release|awk '{print $4}'|awk -v FS="." -v OFS="." '{print $1,$2}')
    fi

    # EulerOS
    if [ "${id}" == "EulerOS" ]; then
        if [ "${ver}" == "2.0" ] && [ "${codename}" == "SP8" ]; then
            version="2.8"
        elif [ "${ver}" == "2.0" ] && [[ "${codename}" =~ SP9 ]]; then
            version="2.9"
        elif [ "${ver}" == "2.0" ] && [[ "${codename}" =~ SP10 ]]; then
            version="2.10"
        fi
    fi

    # Debian
    if [ "${id}" == "Debian" ]; then
        version=$(cat /etc/debian_version)
    fi

    # Kylin
    if [ "${id}" == "Kylin" ]; then
        version=${ver}${codename}
    fi

    # Linx 6 is almost same with debian 9
    if [ "${id}" == "Linx" ]; then
        if [ "${ver}" == "9" ]; then
            version="6.0.90"
        fi
        if [ "${ver}" == "10" ]; then
            version="6.0.100"
        fi
    fi

    # OpenEuler
    if [ "${id}" == "OpenEuler" ]; then
        codename=$(grep -oP "^VERSION=.*\KLTS[-\w]*" /etc/os-release)
        version=${ver}${codename}
    fi

    # UOS 20 SP1
    if [ "${id}" == "UOS" ] && [[ "$(grep -oP "^VERSION=\"?\K[\w\ ]+" /etc/os-release | awk '{print $2}')" == "SP1" ]]; then
        version="${ver}SP1"
    fi

    # UOS 20 1020e
    if [ "${id}" == "UOS" ] && [[ "${kernel_version}" == "4.19.90-2106.3.0.0095.up2.uel20.${arch}" ]]; then
        version="${ver}-1020e"
    fi

    # UOS 20 1021e
    if [ "${id}" == "UOS" ] && [[ "${kernel_version}" == "4.19.90-2109.1.0.0108.up2.uel20.${arch}" ]]; then
        version="${ver}-1021e"
    fi

    echo ${version}
    return 0
}

function get_os_name() {
    local os_id=$(grep -oP "^ID=\"?\K\w+" /etc/os-release)
    local os_name=${OS_MAP[$os_id]}
    echo ${os_name}
}

readonly g_os_name=$(get_os_name)

function get_os_ver_arch() {
    local os_ver=$(grep -oP "^VERSION_ID=\"?\K\w+\.?\w*" /etc/os-release)
    local codename=$(grep -oP "^VERSION=(.*?)\(\K[\w\.\ -]+" /etc/os-release | awk -F_ '{print $1}')
    local os_name=$(get_os_name)
    local version=$(get_os_version ${os_name} ${os_ver} ${codename})
    local os_ver_arch=${g_os_name}_${version}_${arch}
    echo ${os_ver_arch}
    return
}

readonly g_os_ver_arch=$(get_os_ver_arch)

function install_kernel_header_devel_euler() {
    local os_name=$(get_os_name)
    if [ "${os_name}" != "EulerOS" ]; then
        return
    fi
    local euler=""
    if [[ "${g_os_ver_arch}" =~ 2.8 ]]; then
        euler="eulerosv2r8.${arch}"
    elif [[ "${g_os_ver_arch}" =~ 2.9 ]]; then
        euler="eulerosv2r9.${arch}"
    else
        euler="eulerosv2r10.${arch}"
    fi
    local kh=$(rpm -qa kernel-headers | wc -l)
    local kd=$(rpm -qa kernel-devel | wc -l)
    local kh_rpm=$(find ${BASE_DIR}/resources/${g_os_ver_arch}/kernel/ -name "kernel-headers*" | sort -r | grep -m1 ${euler})
    local kd_rpm=$(find ${BASE_DIR}/resources/${g_os_ver_arch}/kernel/ -name "kernel-devel*" | sort -r | grep -m1 ${euler})
    if [ ${kh} -eq 0 ] && [ -f "${kh_rpm}" ]; then
        echo "install ${kh_rpm} when installing system packages" >>${BASE_DIR}/install.log
        rpm -ivh --force --nodeps --replacepkgs ${kh_rpm}
        if [[ $? != 0 ]]; then
            log_error "install kernel_header for euler fail"
            return 1
        fi
    fi
    if [ ${kd} -eq 0 ] && [ -f "${kd_rpm}" ]; then
        echo "install ${kd_rpm} when installing system packages" >>${BASE_DIR}/install.log
        rpm -ivh --force --nodeps --replacepkgs ${kd_rpm}
        if [[ $? != 0 ]]; then
            log_error "install kernel_devel for euler fail"
            return 1
        fi
    fi
}

function install_kernel_header_devel() {
    local have_rpm=$(command -v rpm | wc -l)
    if [ ${have_rpm} -eq 0 ]; then
        return
    fi
    local kh=$(rpm -q kernel-headers | grep ${kernel_version} | wc -l)
    local kd=$(rpm -q kernel-devel | grep ${kernel_version} | wc -l)
    local kh_rpm=${BASE_DIR}/resources/${g_os_ver_arch}/kernel/kernel-headers-${kernel_version}.rpm
    local kd_rpm=${BASE_DIR}/resources/${g_os_ver_arch}/kernel/kernel-devel-${kernel_version}.rpm
    if [ ${kh} -eq 0 ] && [ -f ${kh_rpm} ]; then
        echo "install ${kh_rpm} when installing system packages" >>${BASE_DIR}/install.log
        rpm -ivh --force --nodeps --replacepkgs ${kh_rpm}
        if [[ $? != 0 ]]; then
            log_error "install kernel_header fail"
            return 1
        fi
    fi
    if [ ${kd} -eq 0 ] && [ -f ${kd_rpm} ]; then
        echo "install ${kd_rpm} when installing system packages" >>${BASE_DIR}/install.log
        rpm -ivh --force --nodeps --replacepkgs ${kd_rpm}
        if [[ $? != 0 ]]; then
            log_error "install kernel_devel fail"
            return 1
        fi
    fi
}

# check if resource of specific os is exists
function check_resources() {
    if [ -d ${BASE_DIR}/resources/${g_os_ver_arch} ]; then
        return
    fi
    log_error "Resources missing detected, please run download operation firstly"
    return 1
}

function install_sys_packages() {
    check_resources
    local check_resources_status=$?
    if [[ ${check_resources_status} != 0 ]]; then
        return ${check_resources_status}
    fi

    log_info "install system packages"

    install_kernel_header_devel
    local install_kernel_header_devel_status=$?
    if [[ ${install_kernel_header_devel_status} != 0 ]]; then
        return ${install_kernel_header_devel_status}
    fi

    install_kernel_header_devel_euler
    local install_kernel_header_devel_euler_status=$?
    if [[ ${install_kernel_header_devel_euler_status} != 0 ]]; then
        return ${install_kernel_header_devel_euler_status}
    fi

    local have_rpm=0
    case ${g_os_name} in
    CentOS | EulerOS | Kylin | BCLinux | Tlinux | OpenEuler | CTyunOS)
        local have_rpm=1
        ;;
    Ubuntu | Debian | Linx | UOS)
        local have_rpm=0
        ;;
    *)
        log_error "check OS ${g_os_name} fail"
        return 1
        ;;
    esac
    if [[ "${g_os_ver_arch}" == "Kylin_v10juniper_aarch64" ]]; then
        local have_rpm=0
    fi
    if [[ "${g_os_ver_arch}" == "UOS_20-1020e_${arch}" ]]; then
        local have_rpm=1
    fi
    if [[ "${g_os_ver_arch}" == "UOS_20-1021e_${arch}" ]]; then
        local have_rpm=1
    fi

    echo "install system packages are listed as follows:" >>${BASE_DIR}/install.log
    echo "$(ls ${BASE_DIR}/resources/${g_os_ver_arch} | grep -E "\.(rpm|deb)$")" >>${BASE_DIR}/install.log
    if [ ${have_rpm} -eq 1 ]; then
        rpm -ivh --force --nodeps --replacepkgs ${BASE_DIR}/resources/${g_os_ver_arch}/*.rpm
        if [ $(command -v docker | wc -l) -eq 0 ];then
            rpm -ivh --force --nodeps --replacepkgs ${BASE_DIR}/resources/${g_os_ver_arch}/docker/*.rpm
            systemctl daemon-reload && systemctl restart docker
            echo "install docker success" >>${BASE_DIR}/install.log
        fi
    fi
    if [ ${have_rpm} -ne 1 ]; then
        export DEBIAN_FRONTEND=noninteractive && export DEBIAN_PRIORITY=critical
        dpkg --force-all -i ${BASE_DIR}/resources/${g_os_ver_arch}/*.deb
        if [ $(command -v docker | wc -l) -eq 0 ];then
            dpkg --force-all -i ${BASE_DIR}/resources/${g_os_ver_arch}/docker/*.deb
            systemctl daemon-reload && systemctl restart docker
            echo "install docker success" >>${BASE_DIR}/install.log
        fi
    fi
    if [[ $? != 0 ]]; then
        log_error "install system packages fail"
        return 1
    fi
}

function have_no_python_module() {
    ret=$(python3 -c "import ${1}" 2>&1 | grep "No module" | wc -l)
    return ${ret}
}

function check_python375() {
    if [ ! -d ${PYTHON_PREFIX} ]; then
        log_warning "no ${PYTHON_VERSION} installed"
        return ${FALSE}
    fi
    module_list="ctypes sqlite3 lzma"
    for module in ${module_list}; do
        have_no_python_module ${module}
        ret=$?
        if [ ${ret} == ${TRUE} ]; then
            log_warning "${PYTHON_VERSION} have no moudle ${module}"
            return ${FALSE}
        fi
    done
    if [ $(command -v docker | wc -l) -eq 0 ];then
     return ${FALSE}
    fi
    return ${TRUE}
}

# check if resource of specific os is exists
function check_python_resource() {
    if [ -f ${BASE_DIR}/resources/sources/${PYTHON_TAR}.tar.xz ]; then
        return
    fi
    log_error "Resources missing detected, please run download operation firstly"
    return 1
}

function install_python375() {
    check_python_resource
    local check_python_resource_status=$?
    if [[ ${check_python_resource_status} != 0 ]]; then
        return ${check_python_resource_status}
    fi
    log_info "install ${PYTHON_VERSION}"

    mkdir -p -m 750 ~/build
    tar --no-same-owner -xf ${BASE_DIR}/resources/sources/${PYTHON_TAR}.tar.xz -C ~/build
    cd ~/build/${PYTHON_TAR}
    chmod 750 .
    ./configure --enable-shared --prefix=${PYTHON_PREFIX}
    make -j20
    make install
    cd -
    ${PYTHON_MINOR} -m ensurepip
    ${PYTHON_MINOR} -m pip install --upgrade pip --no-index --find-links ${PYLIB_PATH}
    # install wheel, if not pip will use legacy setup.py install for installation
    ${PYTHON_MINOR} -m pip install wheel --no-index --find-links ${PYLIB_PATH}
    if [[ "${g_os_name}" == "EulerOS" ]] || [[ "${g_os_name}" == "OpenEuler" ]] || [[ "${g_os_ver_arch}" == "UOS_20-1020e_${arch}" ]]; then
        echo "EulerOS or OpenEuler or UOS_20-1020e will install selinux when installing python" >>${BASE_DIR}/install.log
        ${PYTHON_MINOR} -m pip install selinux --no-index --find-links ${PYLIB_PATH}
    fi
    echo "export PATH=${PYTHON_PREFIX}/bin:\$PATH" >${PYTHON_PREFIX}/../ascendrc 2>/dev/null
    echo "export LD_LIBRARY_PATH=${PYTHON_PREFIX}/lib:\$LD_LIBRARY_PATH" >>${PYTHON_PREFIX}/../ascendrc 2>/dev/null
    chmod 640 ${PYTHON_PREFIX}/../ascendrc
}

function bootstrap() {
    unset PYTHONPATH

    check_python375
    local py37_status=$?
    if [ ${py37_status} == ${FALSE} ] && [ $UID -eq 0 ]; then
        install_sys_packages
        local install_sys_packages_status=$?
        if [[ ${install_sys_packages_status} != 0 ]]; then
            return ${install_sys_packages_status}
        fi
        install_python375
        local install_python375_status=$?
        if [[ ${install_python375_status} != 0 ]]; then
            return ${install_python375_status}
        fi
    elif [ ${py37_status} == ${FALSE} ] && [ $UID -ne 0 ]; then
        install_python375
        local install_python375_status_1=$?
        if [[ ${install_python375_status_1} != 0 ]]; then
            return ${install_python375_status_1}
        fi
    fi
    bash ${BASE_DIR}/scripts/install_ansible.sh
}

function set_permission() {
    chmod -R 750 $(find ${BASE_DIR}/ -type d ! -path "${BASE_DIR}/.git*" ! -path "${BASE_DIR}/resources/run_from_*_zip/*") 2>/dev/null
    chmod -R 640 $(find ${BASE_DIR}/ -type f ! -path "${BASE_DIR}/.git*" ! -path "${BASE_DIR}/resources/run_from_*_zip/*") 2>/dev/null
    for f in $(find ${BASE_DIR}/ -maxdepth 2 -type f -name "*.sh" -o -name "*.py" ! -path "${BASE_DIR}/.git*" ! -path "${BASE_DIR}/resources/run_from_*_zip/*"); do
        is_exe=$(file ${f} | grep executable | wc -l)
        if [[ ${is_exe} -eq 1 ]]; then
            chmod 550 ${f} 2>/dev/null
        fi
    done
    chmod 750 $BASE_DIR/ $BASE_DIR/playbooks/install
    chmod 600 ${BASE_DIR}/*.log ${BASE_DIR}/tools/*.log ${BASE_DIR}/inventory_file $BASE_DIR/ansible.cfg ${BASE_DIR}/downloader/config.ini 2>/dev/null
    chmod 400 ${BASE_DIR}/*.log.? ${BASE_DIR}/tools/*.log.? 2>/dev/null
}

main() {
    check_python_version
    local check_python_version_status=$?
    if [[ ${check_python_version_status} != 0 ]]; then
        return ${check_python_version_status}
    fi

    if [ -d ${BASE_DIR}/facts_cache ]; then
        rm -rf ${BASE_DIR}/facts_cache && mkdir -p -m 750 ${BASE_DIR}/facts_cache
    fi

    bootstrap
    local bootstrap_status=$?
    if [[ ${bootstrap_status} != 0 ]]; then
        return ${bootstrap_status}
    fi
}

main $*
main_status=$?
if [[ ${main_status} != 0 ]] && [[ ${main_status} != 6 ]]; then
    operation_log_info "parameter error,run $0 failed"
else
    operation_log_info "$0 $*:Success"
fi
exit ${main_status}
