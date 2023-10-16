current_dir=$(cd $(dirname $0); pwd)
inventory_file_dir=$(cd $current_dir; pwd)
inventory_file_path="$inventory_file_dir/../inventory_file"
yamls_dir=$(cd $current_dir/..; pwd)

readonly PYLIB_PATH_ANSIBLE=${current_dir}/../resources/pylibs
function get_specified_python() {
    if [ ! -z ${ASCEND_PYTHON_VERSION} ]; then
        echo ${ASCEND_PYTHON_VERSION}
    else
        echo $(grep -oP "^ascend_python_version=\K.*" ${current_dir}/../downloader/config.ini | sed 's/\r$//')
    fi
}
readonly specified_python_ansible=$(get_specified_python)

readonly PYTHON_VERSION_ANSIBLE=$(echo ${specified_python_ansible} | sed 's/P/p/;s/-//')

readonly PYTHON_MINOR_ANSIBLE=$(echo ${PYTHON_VERSION_ANSIBLE%.*})

readonly PYTHON_PREFIX_ANSIBLE=${HOME}/.local/${PYTHON_VERSION_ANSIBLE}

export PATH=${PYTHON_PREFIX_ANSIBLE}/bin:$PATH
export LD_LIBRARY_PATH=${PYTHON_PREFIX_ANSIBLE}/lib:$LD_LIBRARY_PATH

bash ${current_dir}/install_ansible.sh && ansible-playbook -i $inventory_file_path $yamls_dir/yamls/hccn.yaml -vv
if [ $? -eq 0 ]; then
    echo "Setting HCCN config success"
else
    echo "Setting HCCN config failed"
fi