#!/bin/bash
readonly SIZE_THRESHOLD=$((5 * 1024 * 1024 * 1024))
readonly ZIP_COUNT_THRESHOLD=3000
readonly TAR_COUNT_THRESHOLD=100000
readonly BASE_DIR=$(dirname $(dirname "$(readlink -f $0)"))
readonly A310P_SOC_PRODUCT_LIST="Ascend-hdk-310p-npu-soc,Ascend-hdk-310p-npu-driver-soc,Ascend-hdk-310p-npu-firmware-soc"
readonly A300I_PRODUCT_LIST="A300i-pro,Atlas-300i-pro"
readonly A300V_PRO_PRODUCT_LIST="A300v-pro,Atlas-300v-pro"
readonly A300V_PRODUCT_LIST="Atlas-300v"
readonly A300IDUO_PRODOUCT_LIST="A300i-duo,Atlas-300i-duo"
readonly A310P_PRODUCT_LIST="Ascend-hdk-310p,Ascend310P"
readonly INFER_PRODUCT_LIST="Ascend-hdk-310,Ascend310,A300-3000,A300-3010,Atlas-200"
readonly NORMALIZE_910_PRODUCT_LIST="Ascend-hdk-910,Ascend910"
readonly TRAIN_910B_PRODUCT_LIST="Ascend-hdk-910b,Ascend910B-hdk"
readonly TRAIN_PRODUCT_LIST="A300t-9000,A800-9000,A800-9010,A900-9000"
readonly TRAIN_PRO_PRODUCT_LIST="Atlas-300t-pro"
readonly CANN_PRODUCT_LIST="Ascend-cann,Ascend-mindx"
readonly A310B_PRODUCT_LIST="Ascend-hdk-310b"

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
readonly ROOT_CA=$(
    cat <<EOF
-----BEGIN CERTIFICATE-----
MIIFTzCCAzegAwIBAgIIRbYUczgwtHkwDQYJKoZIhvcNAQELBQAwNzELMAkGA1UE
BhMCQ04xDzANBgNVBAoTBkh1YXdlaTEXMBUGA1UEAxMOSHVhd2VpIFJvb3QgQ0Ew
IBcNMTUxMDE1MDgwODUwWhgPMjA1MDEwMTUwODA4NTBaMDcxCzAJBgNVBAYTAkNO
MQ8wDQYDVQQKEwZIdWF3ZWkxFzAVBgNVBAMTDkh1YXdlaSBSb290IENBMIICIjAN
BgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA7kxjA5g73QH7nvrTI/ZEJP2Da3Q0
Mg00q8/mM5DAmFkS5/9ru1ZQnKXN5zoq53e4f1r9eUhwjoakWIPjoTdC27hhBoKb
ZbZODbS/uPFu8aXrcDnAnCe+02Dsh5ClHm+Dp37mIe56Nhw/fMVOqZf00cY4GyfJ
KyBRC1cdecg1i2mCApLBe9WZh4/xlmmhCurkl6RyWrXqz6Xmi9glZhlR67g0Y0CU
qtTvyv+GoJyTuH0zq1DUh6VRamKkmoHAMKpDgDfmFkH33UFwgU2X/ef6mJGpYsHu
jlcvon5NZKAYBHmOof2e9mxDyIZH0mZnDsneMF5EDK4jO+qBdFn5KdXy8lOGiVVJ
aeGtux3zG/LgGfil6881mylj3jHszyT0CyIRoQn9HwD5Pn6Punkp5BcyWdzdZ1TF
cBKuIWOGUhbzcFoXnkyz6iDe4gxtH4D3ZQ3x0lpxIHeWUxKl1H0FeoEJx6PL0Koc
/iJ+eMSzoxHx4J5CyTYgF99zpfS7nYXsRhr8y1asXcp7ubLoI8yLkMbBYrg+XFL0
3gOHmkttdX67xKnCxcpYFVWs+nPwyvOCm81SH1YYnJnGP5csjH8hH2xbZpMpwrCZ
n6lZf7tzafmezFgJ6f/A8NZPmzhXe+LXgfWaiE3dBTPFy6ubzBKlWT53BQpP4u11
YvdVxNxSwrKhE4UCAwEAAaNdMFswHwYDVR0jBBgwFoAUcnaWww+QnNRVuK6bSe73
31zJArQwDAYDVR0TBAUwAwEB/zALBgNVHQ8EBAMCAQYwHQYDVR0OBBYEFHJ2lsMP
kJzUVbium0nu999cyQK0MA0GCSqGSIb3DQEBCwUAA4ICAQBwV1EEsMrEarDE0hEq
EyA/N0YpBcUjNWO8UmLYWSzBpv4ePXNtV6PQ8RrGNthcisa56nbb+OfwclPpii01
j89QVI4SlU8BFJUyU/FIRIudlSXWJzAVJcjHatU6Sqi7OdGDoZOIkx0jmyJ5rKoY
oCj4hOjYHeYJIF/CEIF+OnZmj5P6e/MxxC0FvExgJrJyqgIGmRRRkoVEOxjpIHIt
nIFaEa7y8cX9wnvjhYICR6CRmm0jzNsfd0lwdtOedlh3F7nIk8Ot1p3wUMKg1HcM
cxzygWv4CjVTZy6E1/+s6KTEGwX0p/2ISJhfjtlREzvQ6mfwBPbI6NZmD0ymRsy7
mlEEPnkweoEFN9y8P8GITupl20n5C/RD8J+I3ABysW4J57FY6moJawjYvpqGQi+R
4viJ3QWyW+AyMO8hQim924uGNuxij8Avna2K5Mc4Tb/HjSBMJ9glsfTLNqN0xDT7
b7/4o2Fkk5Szt/rKTiSVVbH22US2ri5SV8A+gbH/41NjFNZlAxsxLSN0gHeStDih
kFs9liaQICKYpJToZKHS6hP0paYU61wSqy4lUEyka5KzQZIr7h/BZ8elVI6xGKHg
v2VSpgYKuxC59I+syXRsN6AslVRq8/2Zo1IPcU3k01VsZAlvARrxS+lYfztdiss0
gdNojAmDZwk73Vwty4KrPanEhw==
-----END CERTIFICATE-----
EOF
)

readonly ROOT_CA_G2=$(
    cat <<EOF
-----BEGIN CERTIFICATE-----
MIIGQjCCA/agAwIBAgIDPDrbMEEGCSqGSIb3DQEBCjA0oA8wDQYJYIZIAWUDBAIB
BQChHDAaBgkqhkiG9w0BAQgwDQYJYIZIAWUDBAIBBQCiAwIBIDB8MQswCQYDVQQG
EwJDTjEcMBoGA1UEChMTSHVhd2VpIFRlY2hub2xvZ2llczEnMCUGA1UECxMeSHVh
d2VpIENlcnRpZmljYXRpb24gQXV0aG9yaXR5MSYwJAYDVQQDEx1IdWF3ZWkgSW50
ZWdyaXR5IFJvb3QgQ0EgLSBHMjAgFw0yMTAyMDcwOTM2NDZaGA8yMDUxMDUwNzA5
MzY0NlowfDELMAkGA1UEBhMCQ04xHDAaBgNVBAoTE0h1YXdlaSBUZWNobm9sb2dp
ZXMxJzAlBgNVBAsTHkh1YXdlaSBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTEmMCQG
A1UEAxMdSHVhd2VpIEludGVncml0eSBSb290IENBIC0gRzIwggIiMA0GCSqGSIb3
DQEBAQUAA4ICDwAwggIKAoICAQDdiU8j/HUtpiSLjsmr1t1P/nBDTbxuun0OVcia
Q6Oc+E6y1YXCUmFn+p1WwKEJQetkKbCWlcZch8I2G/f86J/Z4m4ZwZJSV04B/uKQ
GAy35FW5bNBtvYH3xN4ne0oGW6qWkgJQsDHG6iFZqRBKLx1O7yOhwvEdG5jfJwg2
6NK5ad75vM6LHA6tEPG9ttMhcmj9VgzUdAFOHOt1IlAkZ+odFn6Prte4i/M0bYZg
D/LShlgtBp+iDrWD+zHfcWADEGEsEzxyX7CJviJBTnoUwKM0/CQGLzaUTcGKfmVR
qvlxCuSGRYsZWlOyoGomiSzmHxCMKzshrHW+RTO6YidFvbt/eKM0TRl3sXm6S1+C
+FRY25es4lrXBm1/7VIcYy8CAmBAzYscFkaJqDiOqZ2wH3nDmonZeLgL0gfhSN5X
ofsOa3+K0FwLGMSs8S6znSyFdmgsdAu53EzQQ/CDolyDKza38sqRMxa2FSvIrbji
lypuUg6QH4p8XZdLac/D63s69rVbDgct9Yt39e7PCx51XLkQZevzW0wacuylvzyW
TCHqvNHo3zVLvfhtfB70LkhTTnZIcJFSi/Qz62BfQwBriMLEtNaFDyVA1/ZyJLPa
O0NvQ7T2tkkfsopSjGq8U9bcirLLyIJT3PW5j+zr96cO4nnO6TK2esXnBC6m/tqr
NhKnQwIDAQABo2MwYTAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUwAwEB/zAd
BgNVHQ4EFgQUDjkBfSbLAmrgyjRlUCChRGzsf54wHwYDVR0jBBgwFoAUDjkBfSbL
AmrgyjRlUCChRGzsf54wQQYJKoZIhvcNAQEKMDSgDzANBglghkgBZQMEAgEFAKEc
MBoGCSqGSIb3DQEBCDANBglghkgBZQMEAgEFAKIDAgEgA4ICAQBhnanpVOz0exdF
fSyv8VxBZKL0XIYDue5nmeo0CJ2770Tj6NZawOJPkOAluzSAJpGKZdZgTfZdjKgR
UmGAzL0IBdOf2lbmRyz4Qm1e6nTqB6TvveyeksnxfxDAQq0t2zbIv41OS3RObf5C
T56TKR7mp7t6QR83Er8zaK8WbehFMx0puRTt+kST7b32Nzp2jI7jxlugi7+/oJoR
dwYd7NKTdkpjLSBz3dfigt2Gp8U5BTXxAvO6hsVkb4OHbJ5n+h5avY8q/Hzzd2xc
7bJFHVy5pL4nh/vM1z8/MRZUpxGLKOozNarYESVSzIZc9ovA08WKmaSqXkCgNwEv
7K/cDCnKAp73aknUAGJg6zAN3BZikSLYM+V+Tmc4FR/UQG/+GSkdvg0kmxKt3izw
oVctj/Je350VQLOgYkmOTQXdBCtMo8T5q/ZWq8mct1DtS4KaLxgLQQN214QS5MqY
68mFyuU3eKN7sD7BUzhG6t+phVhFJ6mslPOpaxOSaUFwBXW1nZ4afoKrk7EFXVQ1
xr37Fsc+a2P7DF9GD4liyzLc+0xOJZRVrM7fNPbdID0a2gp65qyTK4wrD/xsS7c6
NtAPvl8SX/H76yV7/XFtqmmfRj3YyGj2DctWZ8qUVTsxHQxVMWkeFzf7G4au6jqn
UCrZxwwkrbPM3H6LA3VdrF1oWN0hjg==
-----END CERTIFICATE-----
EOF
)

function check_extracted_size() {
    local IFS_OLD=$IFS
    unset IFS
    for zip_package in $(find ${BASE_DIR}/resources/ -name "*.zip" 2>/dev/null); do
        unzip -l ${zip_package} >/dev/null 2>&1
        if [[ $? != 0 ]]; then
            log_error "$(basename ${zip_package}) does not look like a zip compressed file"
            return 1
        fi
        local check_zip=$(unzip -l ${zip_package} | awk -v size_threshold="${SIZE_THRESHOLD}" -v count_threshold="${ZIP_COUNT_THRESHOLD}" 'END {print ($1 <= size_threshold && $2 <= count_threshold)}')
        if [[ ${check_zip} == 0 ]]; then
            log_error "$(basename ${zip_package}) extracted size over 5G or extracted files count over ${ZIP_COUNT_THRESHOLD}"
            return 1
        fi
        unzip -l ${zip_package} | grep -F "../" >/dev/null 2>&1
        if [[ $? == 0 ]]; then
            log_error "The name of $(basename ${zip_package}) contains ../"
            return 1
        fi
        unzip -l ${zip_package} | grep -F '..\' >/dev/null 2>&1
        if [[ $? == 0 ]]; then
            log_error "The name of $(basename ${zip_package}) contains ..\\"
            return 1
        fi
    done
    for tar_package in $(find ${BASE_DIR}/resources/ -type f -name "*.tar" -o -name "*.tar.*z*" 2>/dev/null); do
        tar tvf ${tar_package} >/dev/null 2>&1
        if [[ $? != 0 ]]; then
            log_error "$(basename ${tar_package}) does not look like a tar compressed file"
            return 1
        fi
        local check_tar=$(tar tvf ${tar_package} | awk -v size_threshold="${SIZE_THRESHOLD}" -v count_threshold="${TAR_COUNT_THRESHOLD}" '{sum += $3} END {print (sum <= size_threshold && NR <= count_threshold)}')
        if [[ ${check_tar} == 0 ]]; then
            log_error "$(basename ${tar_package}) extracted size over 5G or extracted files count over ${TAR_COUNT_THRESHOLD}"
            return 1
        fi
        tar tf ${tar_package} | grep -F "../" >/dev/null 2>&1
        if [[ $? == 0 ]]; then
            log_error "The name of $(basename ${tar_package}) contains ../"
            return 1
        fi
        tar tf ${tar_package} | grep -F '..\' >/dev/null 2>&1
        if [[ $? == 0 ]]; then
            log_error "The name of $(basename ${tar_package}) contains ..\\"
            return 1
        fi
    done
    IFS=${IFS_OLD}
}
function check_npu_scene() {
    IFS=","
    for product in $1; do
        if [[ "$2" =~ ${product} ]]; then
            echo 1
            unset IFS
            return 0
        fi
    done
    echo 0
    unset IFS
    return 0
}

function check_run_pkg() {
    if [[ "$(basename ${run_file})" =~ run ]]; then
        if [[ $(check_npu_scene ${CANN_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_cann_zip
        elif [[ $(check_npu_scene ${A310P_SOC_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_soc_zip
        elif [[ $(check_npu_scene ${A300I_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_a300i_zip
        elif [[ $(check_npu_scene ${A300V_PRO_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_a300v_pro_zip
        elif [[ $(check_npu_scene ${A300V_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_a300v_zip
        elif [[ $(check_npu_scene ${A300IDUO_PRODOUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_a300iduo_zip
        elif [[ $(check_npu_scene ${A310P_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_a310p_zip
        elif [[ $(check_npu_scene ${INFER_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_infer_zip
        elif [[ $(check_npu_scene ${TRAIN_910B_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_910b_zip
        elif [[ $(check_npu_scene ${TRAIN_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_train_zip
        elif [[ $(check_npu_scene ${TRAIN_PRO_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_train_pro_zip
        elif [[ $(check_npu_scene ${NORMALIZE_910_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_910_zip
        elif [[ $(check_npu_scene ${A310B_PRODUCT_LIST} $(basename ${run_file})) == 1 ]]; then
            local run_pkg_dir=${BASE_DIR}/resources/run_from_310b_zip
        else
            echo "not support $(basename ${run_file}), please check" >>${BASE_DIR}/install.log
            return 1
        fi
        mkdir -p -m 750 ${run_pkg_dir} && cp ${run_file} ${run_pkg_dir}
    fi
}

function check_run_pkgs() {
    unset IFS
    rm -rf ${BASE_DIR}/resources/run_from_*_zip
    for run_file in $(
        find ${BASE_DIR}/resources/CANN_* 2>/dev/null | grep ".run$"
        find ${BASE_DIR}/resources/npu 2>/dev/null | grep ".run$"
        find ${BASE_DIR}/resources/*.run 2>/dev/null
        find ${BASE_DIR}/resources/patch/*.run 2>/dev/null
    ); do
        check_run_pkg
    done
}
function zip_extract() {
    if [[ "$(basename ${zip_file})" =~ zip ]]; then
        if [[ $(check_npu_scene ${CANN_PRODUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_cann_zip
        elif [[ $(check_npu_scene ${A310P_SOC_PRODUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_soc_zip
        elif [[ $(check_npu_scene ${A300I_PRODUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_a300i_zip
        elif [[ $(check_npu_scene ${A300V_PRO_PRODUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_a300v_pro_zip
        elif [[ $(check_npu_scene ${A300V_PRODUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_a300v_zip
        elif [[ $(check_npu_scene ${A300IDUO_PRODOUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_a300iduo_zip
        elif [[ $(check_npu_scene ${A310P_PRODUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_a310p_zip
        elif [[ $(check_npu_scene ${INFER_PRODUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_infer_zip
        elif [[ $(check_npu_scene ${TRAIN_910B_PRODUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_910b_zip
        elif [[ $(check_npu_scene ${TRAIN_PRODUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_train_zip
        elif [[ $(check_npu_scene ${TRAIN_PRO_PRODUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_train_pro_zip
        elif [[ $(check_npu_scene ${NORMALIZE_910_PRODUCT_LIST} $(basename ${zip_file})) == 1 ]]; then
            local run_from_zip=${BASE_DIR}/resources/run_from_910_zip
        else
            echo "not support $(basename ${zip_file}), please check" >>${BASE_DIR}/install.log
            return 1
        fi
        mkdir -p -m 750 ${run_from_zip} && unzip -oq ${zip_file} -d ${run_from_zip}
    else
        if [[ "$(basename ${zip_file})" =~ atlasedge.*aarch64 ]]; then
            local atlasedge_dir=${BASE_DIR}/resources/run_from_cann_zip/atlasedge_aarch64
        elif [[ "$(basename ${zip_file})" =~ ha.*aarch64 ]]; then
            local atlasedge_dir=${BASE_DIR}/resources/run_from_cann_zip/ha_aarch64
        elif [[ "$(basename ${zip_file})" =~ atlasedge.*x86_64 ]]; then
            local atlasedge_dir=${BASE_DIR}/resources/run_from_cann_zip/atlasedge_x86_64
        elif [[ "$(basename ${zip_file})" =~ ha.*x86_64 ]]; then
            local atlasedge_dir=${BASE_DIR}/resources/run_from_cann_zip/ha_x86_64
        elif [[ "$(basename ${zip_file})" =~ 310b ]]; then
            local atlasedge_dir=${BASE_DIR}/resources/run_from_310b_zip
        fi
        mkdir -p -m 750 ${atlasedge_dir}
        cp ${zip_file} ${cms_file} ${crl_file} ${atlasedge_dir}
        tar --no-same-owner -xf ${zip_file} -C ${atlasedge_dir}
    fi
}

function compare_crl() {
    openssl crl -verify -in $1 -inform DER -CAfile $3 -noout 2>/dev/null
    if [[ $? != 0 ]]; then
        echo "$(basename $3) check $(basename $1) validation not pass" >>${BASE_DIR}/install.log
        return 2
    fi
    if [[ -f $2 ]]; then
        openssl crl -verify -in $2 -inform DER -CAfile $3 -noout 2>/dev/null
        if [[ $? != 0 ]]; then
            echo "$(basename $3) check $(basename $2) validation not pass" >>${BASE_DIR}/install.log
            return 3
        fi
        local zip_crl_lastupdate_time=$(date +%s -d "$(openssl crl -in $1 -inform DER -noout -lastupdate | awk -F'lastUpdate=' '{print $2}')")
        local sys_crl_lastupdate_time=$(date +%s -d "$(openssl crl -in $2 -inform DER -noout -lastupdate | awk -F'lastUpdate=' '{print $2}')")
        if [[ ${zip_crl_lastupdate_time} -gt ${sys_crl_lastupdate_time} ]]; then
            echo "$(basename $2) system crl update success" >>${BASE_DIR}/install.log
            mkdir -p -m 700 $(dirname $2) && cp $1 $2 && chmod 600 $2
            return 0
        elif [[ ${zip_crl_lastupdate_time} -eq ${sys_crl_lastupdate_time} ]]; then
            return 0
        else
            echo "$(basename $2) is newer than $(basename $1), no need to update system crl" >>${BASE_DIR}/install.log
            return 1
        fi
    else
        echo "$(basename $2) system crl update success" >>${BASE_DIR}/install.log
        mkdir -p -m 700 $(dirname $2) && cp $1 $2 && chmod 600 $2
    fi
    return 0
}
function hmac_check() {
    local sys_crl=$1
    local ca_file=$2
    compare_crl ${crl_file} ${sys_crl} ${ca_file}
    local verify_crl=$?
    if [[ ${verify_crl} == 0 ]]; then
        local updated_crl=${crl_file}
    elif [[ ${verify_crl} == 1 ]]; then
        local updated_crl=${sys_crl}
    else
        return 1
    fi
    [[ ! "$(openssl crl -in ${updated_crl} -inform DER -noout -text)" =~ "$(openssl x509 -in ${ca_file} -serial -noout | awk -F'serial=' '{print $2}')" ]] &&
        openssl cms -verify --no_check_time -in ${cms_file} -inform DER -CAfile ${ca_file} -binary -content ${zip_file} -purpose any -out /dev/null 2>/dev/null
    local verify_success=$?
    if [[ ${verify_success} -ne 0 ]]; then
        echo "$(basename ${updated_crl}) or $(basename ${cms_file}) check cms validation not pass for $(basename ${ca_file})" >>${BASE_DIR}/install.log
        return 1
    fi
}

function verify_zip() {
    unset IFS
    local hmac_check_result=0
    if [[ ${UID} == 0 ]]; then
        local sys_crl_file=/etc/hwsipcrl/ascendsip.crl
        local sys_g2_crl_file=/etc/hwsipcrl/ascendsip_g2.crl
        local ascend_cert_path=/usr/local/Ascend/toolbox/latest/Ascend-DMI/bin/ascend-cert
    else
        local sys_crl_file=~/.local/hwsipcrl/ascendsip.crl
        local sys_g2_crl_file=~/.local/hwsipcrl/ascendsip_g2.crl
        local ascend_cert_path=~/Ascend/toolbox/latest/Ascend-DMI/bin/ascend-cert
    fi
    local root_ca_g2_file=${BASE_DIR}/playbooks/rootca_g2.pem
    echo -e "${ROOT_CA_G2}" >${root_ca_g2_file}
    local root_ca_file=${BASE_DIR}/playbooks/rootca.pem
    echo -e "${ROOT_CA}" >${root_ca_file}
    chmod 600 ${root_ca_g2_file} ${root_ca_file}
    for zip_package in $(
        find ${BASE_DIR}/resources/CANN_* 2>/dev/null | grep ".zip$"
        find ${BASE_DIR}/resources/npu 2>/dev/null | grep ".zip$"
        find ${BASE_DIR}/resources/*.zip 2>/dev/null
        find ${BASE_DIR}/resources/patch/*.zip 2>/dev/null
    ); do
        rm -rf ${BASE_DIR}/resources/zip_tmp && unzip -q ${zip_package} -d ${BASE_DIR}/resources/zip_tmp
        local cms_file=$(find ${BASE_DIR}/resources/zip_tmp/*.zip.cms 2>/dev/null || find ${BASE_DIR}/resources/zip_tmp/*.tar.gz.cms 2>/dev/null)
        local zip_file=$(find ${BASE_DIR}/resources/zip_tmp/*.zip 2>/dev/null || find ${BASE_DIR}/resources/zip_tmp/*.tar.gz 2>/dev/null)
        local crl_file=$(find ${BASE_DIR}/resources/zip_tmp/*.zip.crl 2>/dev/null || find ${BASE_DIR}/resources/zip_tmp/*.tar.gz.crl 2>/dev/null)
        chmod 600 ${cms_file} ${zip_file} ${crl_file}
        if [ -f ${ascend_cert_path} ]; then
            echo "ascend-cert check $(basename ${zip_file})" >>${BASE_DIR}/install.log
            ${ascend_cert_path} -u ${crl_file} >/dev/null 2>&1
            if [[ $? != 0 ]]; then
                echo "ascend-cert update $(basename ${crl_file}) to system failed" >>${BASE_DIR}/install.log
                hmac_check_result=1
            else
                ${ascend_cert_path} ${cms_file} ${zip_file} ${crl_file} >/dev/null 2>&1
                hmac_check_result=$?
            fi
        else
            echo "openssl check $(basename ${zip_file})" >>${BASE_DIR}/install.log
            hmac_check ${sys_g2_crl_file} ${root_ca_g2_file} || hmac_check ${sys_crl_file} ${root_ca_file}
            hmac_check_result=$?
        fi
        if [[ ${hmac_check_result} == 0 ]]; then
            zip_extract
            rm -rf ${BASE_DIR}/resources/zip_tmp
        else
            rm -rf ${BASE_DIR}/resources/zip_tmp
            break
        fi
    done
    rm -rf ${root_ca_g2_file} ${root_ca_file}
    chmod -R 750 $(find ${BASE_DIR}/resources/run_from_*_zip -type d 2>/dev/null) 2>/dev/null
    chmod -R 640 $(find ${BASE_DIR}/resources/run_from_*_zip -type f 2>/dev/null) 2>/dev/null
    return ${hmac_check_result}
}
function verify_zip_redirect() {
    log_info "The system is busy with checking compressed files, Please wait for a moment..."
    rm -rf ${BASE_DIR}/resources/zip_tmp
    check_extracted_size
    local check_extracted_size_status=$?
    if [[ ${check_extracted_size_status} != 0 ]]; then
        return ${check_extracted_size_status}
    fi
    verify_zip >${BASE_DIR}/tmp.log 2>&1
    local verify_result=$?
    cat ${BASE_DIR}/tmp.log >>${BASE_DIR}/install.log
    cat ${BASE_DIR}/tmp.log && rm -rf ${BASE_DIR}/tmp.log
    if [ ${verify_result} -ne 0 ]; then
        log_error "check validation fail"
        return 1
    fi
    if [[ $(find ${BASE_DIR}/resources -type f | wc -L) -gt 1023 ]] || [[ $(find ${BASE_DIR}/resources -type l | wc -L) -gt 1023 ]]; then
        log_error "The file name contains more than 1023 characters"
        return 1
    fi
}

function main() {
    check_run_pkgs
    verify_zip_redirect
    local verify_zip_redirect_status=$?
    if [[ ${verify_zip_redirect_status} != 0 ]]; then
        return ${verify_zip_redirect_status}
    fi
}

main
