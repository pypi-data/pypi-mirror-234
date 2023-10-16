# Copyright 2020 Huawei Technologies Co., Ltd
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
"""download os dependencies"""
import json
import os

from . import logger_config
from .deb_downloader import Apt
from .download_data import DownloadData
from .download_util import get_download_path
from .rpm_downloader import Yum

LOG = logger_config.LOG


class OsDepDownloader:
    def __init__(self, download_data: DownloadData):
        self.software_mgr = download_data.software_mgr
        self.project_dir = get_download_path()
        self.resources_dir = os.path.join(self.project_dir, 'resources')

    def download(self, os_list, software_list, dst):
        results = {}
        mindstudio_list = [software for software in software_list if "MindStudio" in software]
        for os_item in os_list:
            res = self.download_os(os_item, mindstudio_list, dst)
            results[os_item] = res
        return results

    def download_os(self, os_item, software_list, dst):
        """
        download os packages. debs or rpms
        :param os_itme:  Ubuntu_18.04_aarch64, CentOS_8.2_x86_64..
        """
        docker_pkg_list = [
            "docker-ce-cli",
            "containerd.io",
            "docker-ce",
            "docker-ce-rootless-extras",
            "docker-scan-plugin",
            "docker-engine",
        ]
        dst_dir = os.path.join(dst, os_item)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir, mode=0o750, exist_ok=True)
        docker_dir = os.path.join(dst_dir, 'docker')
        if not os.path.exists(docker_dir):
            os.makedirs(docker_dir, mode=0o750, exist_ok=True)
        LOG.info('item:{} save dir: {}'.format(os_item, os.path.basename(dst_dir)))

        config_file = os.path.join(self.project_dir, 'downloader/config/{0}/pkg_info.json'.format(os_item))
        source_list_file = os.path.join(self.project_dir, 'downloader/config/{0}/source.list'.format(os_item))
        downloader = None

        if os.path.exists(source_list_file):
            if 'aarch64' in os_item:
                downloader = Apt(source_list_file, 'aarch64')
            else:
                downloader = Apt(source_list_file, 'x86_64')
        else:
            source_repo_file = os.path.join(self.project_dir, 'downloader/config/{0}/source.repo'.format(os_item))
            if 'aarch64' in os_item:
                downloader = Yum(source_repo_file, 'aarch64')
            else:
                downloader = Yum(source_repo_file, 'x86_64')

        res = {'ok': [], 'failed': []}
        if downloader is not None:
            if downloader.make_cache() is False:
                LOG.error('downloader make_cache failed')
                res.get('failed', []).append(os_item)
                raise RuntimeError

        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                if item['name'] in docker_pkg_list:
                    dst_dir = docker_dir
                else:
                    dst_dir = os.path.join(dst, os_item)
                if downloader.download(item, dst_dir):
                    res.get('ok', []).append(item['name'])
                    continue
                print('download failed', item['name'])
                res.get('failed', []).append(item['name'])
                raise RuntimeError

        for software in software_list:
            formal_name, version = self.software_mgr.get_software_name_version(software)
            pkg_list = self.software_mgr.get_software_sys(formal_name, os_item, version)
            soft_dst_dir = os.path.join(dst, "{0}_{1}".format(formal_name, version), os_item)
            for pkg_obj in pkg_list:
                pkg = json.loads(str(pkg_obj))
                if downloader.download(pkg, soft_dst_dir):
                    res.get('ok', []).append(pkg['name'])
                    continue
                print('download failed', pkg['name'])
                res.get('failed', []).append(pkg['name'])
        if downloader is not None:
            downloader.clean_cache()
        return res
