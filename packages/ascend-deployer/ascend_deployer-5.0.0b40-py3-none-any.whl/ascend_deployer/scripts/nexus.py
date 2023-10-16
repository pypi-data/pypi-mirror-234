#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================
import base64
import glob
import json
import os
import platform
import re
import secrets
import shlex
import shutil
import string
import subprocess
import time
from urllib import parse, request


def get_passwd():
    return "".join(
        secrets.choice(string.digits + string.ascii_letters)
        for _ in range(16)
    )


class OsRepository:
    NEXUS_USER = "admin"
    NEXUS_RUN_PORT = 58081
    nexus_passwd = get_passwd()
    gpg_passwd = get_passwd()

    def __init__(self):
        try:
            self.nexus_run_ip = os.environ["SSH_CONNECTION"].split()[2]
            self.working_on_ipv6 = False
            if ":" in self.nexus_run_ip:  # ipv6格式需要用括号包住域名部分
                self.nexus_run_ip = "[%s]" % self.nexus_run_ip
                self.working_on_ipv6 = True
        except KeyError:
            raise RuntimeError("Do not switch users after SSH connection")
        self.root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.config = f"{self.root_dir}/scripts/nexus_config.json"
        self.arch = platform.machine()
        os.environ.pop("http_proxy", "")
        os.environ.pop("https_proxy", "")
        with open(self.config, "r", encoding="utf-8") as f:
            self.config_content = json.load(f)
        self.nexus_data_dir = os.path.join("/tmp", "nexus-data")
        self.nexus_image_name = self.config_content.get("image")
        try:
            self.nexus_image = glob.glob(
                f'{os.path.join(self.root_dir, "resources", "nexus")}/nexus*{self.arch}.tar'
            )[0]
        except IndexError:
            raise FileNotFoundError("nexus image does not exist") from None
        auth = base64.b64encode(
            f"{self.NEXUS_USER}:{self.nexus_passwd}".encode("utf-8")
        ).decode("utf-8")
        self.post_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
        }
        self.upload_headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/octet-stream",
        }

    @staticmethod
    def _delete_nexus_container():
        container_info = "docker ps -a"
        try:
            info_result = subprocess.run(
                shlex.split(container_info),
                shell=False,
                encoding="utf-8",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
        except FileNotFoundError:
            raise FileNotFoundError("Please install Docker first")
        except subprocess.CalledProcessError:
            raise RuntimeError("Docker not available")
        else:
            if "nexus" in info_result.stdout.split():
                delete_cmd = "docker rm -f nexus"
                subprocess.run(
                    shlex.split(delete_cmd),
                    shell=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            subprocess.run(
                shlex.split("docker network rm ip6net_nexus"),
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    @staticmethod
    def _check_nexus_status():
        check_cmd = "docker logs nexus"
        timeout = 0
        while True:
            time.sleep(10)
            timeout += 10
            nexus_status = subprocess.run(
                shlex.split(check_cmd),
                shell=False,
                stdout=subprocess.PIPE,
                encoding="utf-8",
                check=True,
            )
            if "Nexus OSS" in nexus_status.stdout:
                break
            if timeout >= 120:
                raise TimeoutError("Nexus startup timeout")

    def init_nexus(self):
        self._run_nexus()
        self._check_nexus_status()
        tmp_passwd_file = f"{self.nexus_data_dir}/admin.password"
        with open(tmp_passwd_file, "r", encoding="utf-8") as f:
            old_passwd = f.read()
        auth = base64.b64encode(
            f"{self.NEXUS_USER}:{old_passwd}".encode("utf-8")
        ).decode("utf-8")
        headers = {
            "accept": "application/json",
            "Content-Type": "text/plain",
            "Authorization": f"Basic {auth}",
        }
        url = f"http://{self.nexus_run_ip}:{self.NEXUS_RUN_PORT}/service/rest/v1/security/users/admin/change-password"
        req = request.Request(
            url,
            data=self.nexus_passwd.encode("utf-8"),
            headers=headers,
            method="PUT",
        )
        request.urlopen(req)

        url = f"http://{self.nexus_run_ip}:{self.NEXUS_RUN_PORT}/service/rest/v1/security/anonymous"
        data = {
            "enabled": True,
            "userId": "anonymous",
            "realmName": "NexusAuthorizingRealm",
        }
        req = request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=self.post_headers,
            method="PUT",
        )
        request.urlopen(req)

    def get_download_os_info(self):
        os_list_dir = f"{self.root_dir}/resources"
        os_list = [os_item for os_item in glob.glob(f"{os_list_dir}/*aarch64")]
        os_list.extend(os_item for os_item in glob.glob(f"{os_list_dir}/*x86_64"))
        return os_list

    def get_os_files(self, os_dir):
        files = []
        for file_name in os.listdir(os_dir):
            file_path = os.path.join(os_dir, file_name)
            if os.path.isdir(file_path):
                files.extend(self.get_os_files(file_path))
            else:
                files.append(file_path)
        return files

    def _create_data_dir(self):
        try:
            os.makedirs(self.nexus_data_dir, mode=0o700)
        except FileExistsError:
            try:
                shutil.rmtree(self.nexus_data_dir)
            except OSError:
                umount_data_dir_cmd = f"umount {self.nexus_data_dir}"
                subprocess.run(shlex.split(umount_data_dir_cmd), shell=False, stderr=subprocess.DEVNULL)
                shutil.rmtree(self.nexus_data_dir)
            finally:
                os.makedirs(self.nexus_data_dir, mode=0o700)
        os.chown(self.nexus_data_dir, 200, 200)
        mount_data_dir_cmd = f"mount -t tmpfs tmpfs {self.nexus_data_dir}"
        subprocess.run(shlex.split(mount_data_dir_cmd), shell=False, check=True)

    def _run_nexus(self):
        self._delete_nexus_container()
        self._create_data_dir()
        network_command_opt = ""
        if self.working_on_ipv6:
            if not os.path.exists("/etc/docker/daemon.json"):
                os.makedirs("/etc/docker/", mode=0o755, exist_ok=True)
                with open("/etc/docker/daemon.json", "w") as fid:
                    json.dump({}, fid, indent=1)
            with open("/etc/docker/daemon.json") as fid:
                docker_settings = json.load(fid)
            docker_settings["experimental"] = True
            docker_settings["ip6tables"] = True
            with open("/etc/docker/daemon.json", "w") as fid:
                json.dump(docker_settings, fid, indent=1)
            subprocess.getoutput("systemctl restart docker")
            subprocess.getoutput("docker network create --ipv6 --subnet 2001:0DB8::/112 ip6net_nexus")
            network_command_opt = "--network ip6net_nexus"
        load_cmd = f"docker load -i {self.nexus_image}"
        subprocess.run(shlex.split(load_cmd), shell=False, stdout=subprocess.DEVNULL)
        run_cmd = (
            f"docker run -d --name nexus {network_command_opt} -p {self.NEXUS_RUN_PORT}:8081 "
            f"-v {self.nexus_data_dir}:/nexus-data {self.nexus_image_name}"
        )
        subprocess.run(
            shlex.split(run_cmd), shell=False, check=True, stdout=subprocess.DEVNULL
        )


class YumRepository(OsRepository):
    def create_blob(self):
        url = f"http://{self.nexus_run_ip}:{self.NEXUS_RUN_PORT}/service/rest/v1/blobstores/file"
        data = {"softQuota": None, "path": "/nexus-data/blobs/yum", "name": "yum"}
        req = request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=self.post_headers,
            method="POST",
        )
        request.urlopen(req)

    def create_repository(self):
        url = f"http://{self.nexus_run_ip}:{self.NEXUS_RUN_PORT}/service/rest/v1/repositories/yum/hosted"
        os_info = self.get_download_os_info()
        for i in os_info:
            repository_name = os.path.basename(i)
            if repository_name in self.config_content["rpm_os"]:
                data = {
                    "name": repository_name,
                    "online": True,
                    "storage": {
                        "blobStoreName": "yum",
                        "strictContentTypeValidation": True,
                        "writePolicy": "ALLOW",
                    },
                    "cleanup": None,
                    "component": {
                        "proprietaryComponents": False,
                    },
                    "yum": {"repodataDepth": 0, "deployPolicy": "STRICT"},
                }
                req = request.Request(
                    url,
                    data=json.dumps(data).encode("utf-8"),
                    headers=self.post_headers,
                    method="POST",
                )
                request.urlopen(req)

    def upload_rpm(self):
        base_url = f"http://{self.nexus_run_ip}:{self.NEXUS_RUN_PORT}/repository/"
        download_os_list = self.get_download_os_info()
        for i in download_os_list:
            os_name = os.path.basename(i)
            if os_name not in self.config_content["rpm_os"]:
                continue
            os_deps = self.get_os_files(i)
            if "CentOS_7.6" in os_name:
                os_deps = [os_dep for os_dep in os_deps if not re.search(r"openssl.*1.1.1", os_dep)]
            for j in os_deps:
                with open(j, "rb") as f:
                    file_content = f.read()
                url = parse.urljoin(
                    base_url, f"{os.path.basename(i)}/{os.path.basename(j)}"
                )
                req = request.Request(
                    url, data=file_content, headers=self.upload_headers, method="PUT"
                )
                request.urlopen(req)


class AptRepository(OsRepository):
    def generate_gpg_key(self):
        gpg_dir = f"{os.environ['HOME']}/.gnupg"
        if os.path.exists(gpg_dir):
            shutil.rmtree(gpg_dir)
        base_cmd = "gpg --gen-key --batch"
        gpg_data = f"""Key-Type: RSA
        Key-Length: 3072
        Name-Real: nexus
        Expire-Date: 3d
        Passphrase: {self.gpg_passwd}
        """
        subprocess.run(
            shlex.split(base_cmd),
            input=gpg_data.encode("utf-8"),
            shell=False,
            check=True,
        )

    def export_gpg_key(self):
        gpg_key_dir = os.path.dirname(self.nexus_image)
        gpg_pub_key = f"{gpg_key_dir}/nexus_pub.asc"
        gpg_pri_key = f"{gpg_key_dir}/nexus_pri.asc"
        if os.path.exists(gpg_pub_key):
            os.unlink(gpg_pub_key)
        if os.path.exists(gpg_pri_key):
            os.unlink(gpg_pri_key)
        export_public_key_cmd = f"gpg -a -o {gpg_pub_key} --export nexus"
        export_private_key_cmd = (
            f"gpg --batch --pinentry-mode=loopback --yes --passphrase {self.gpg_passwd} "
            f"-a -o {gpg_pri_key} --export-secret-key nexus"
        )
        subprocess.run(
            shlex.split(export_public_key_cmd),
            shell=False,
            check=True,
        )
        subprocess.run(
            shlex.split(export_private_key_cmd),
            shell=False,
            check=True,
        )
        with open(gpg_pri_key, "r", encoding="utf-8") as f:
            gpg_pri_content = f.read()
        return gpg_pri_content

    def create_blob(self):
        url = f"http://{self.nexus_run_ip}:{self.NEXUS_RUN_PORT}/service/rest/v1/blobstores/file"
        data = {"softQuota": None, "path": "/nexus-data/blobs/apt", "name": "apt"}
        req = request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=self.post_headers,
            method="POST",
        )
        request.urlopen(req)

    def create_repository(self, keypair):
        url = f"http://{self.nexus_run_ip}:{self.NEXUS_RUN_PORT}/service/rest/v1/repositories/apt/hosted"
        os_info = self.get_download_os_info()
        for i in os_info:
            repository_name = os.path.basename(i)
            if repository_name in self.config_content["deb_os"]:
                codename = self.config_content["codename"][repository_name]
                data = {
                    "name": repository_name,
                    "online": True,
                    "storage": {
                        "blobStoreName": "apt",
                        "strictContentTypeValidation": True,
                        "writePolicy": "ALLOW",
                    },
                    "cleanup": None,
                    "component": {
                        "proprietaryComponents": False,
                    },
                    "apt": {"distribution": codename},
                    "aptSigning": {"keypair": keypair, "passphrase": self.gpg_passwd},
                }
                req = request.Request(
                    url,
                    data=json.dumps(data).encode("utf-8"),
                    headers=self.post_headers,
                    method="POST",
                )
                request.urlopen(req)

    def upload_deb(self):
        base_url = f"http://{self.nexus_run_ip}:{self.NEXUS_RUN_PORT}/repository/"
        download_os_list = self.get_download_os_info()
        for i in download_os_list:
            if os.path.basename(i) not in self.config_content["deb_os"]:
                continue
            os_deps = self.get_os_files(i)
            for j in os_deps:
                with open(j, "rb") as f:
                    file_content = f.read()
                url = parse.urljoin(base_url, f"{os.path.basename(i)}/")
                req = request.Request(
                    url,
                    data=file_content,
                    headers=self.upload_headers,
                    method="POST",
                )
                request.urlopen(req)


def main():
    yum_repository = YumRepository()
    download_os_list = [
        os.path.basename(i)
        for i in yum_repository.get_download_os_info()
    ]
    have_rpm = any(
        os_item in yum_repository.config_content["rpm_os"]
        for os_item in download_os_list
    )
    have_deb = any(
        os_item in yum_repository.config_content["deb_os"]
        for os_item in download_os_list
    )
    yum_repository.init_nexus()
    if have_rpm:
        yum_repository.create_blob()
        yum_repository.create_repository()
        yum_repository.upload_rpm()
    if have_deb:
        centos_release = "/etc/centos-release"
        if os.path.exists(centos_release):
            return
        apt_repository = AptRepository()
        apt_repository.create_blob()
        apt_repository.generate_gpg_key()
        gpg_pair_key = apt_repository.export_gpg_key()
        if gpg_pair_key == "":
            raise RuntimeError("The file content is empty")
        apt_repository.create_repository(gpg_pair_key)
        apt_repository.upload_deb()


if __name__ == "__main__":
    main()
