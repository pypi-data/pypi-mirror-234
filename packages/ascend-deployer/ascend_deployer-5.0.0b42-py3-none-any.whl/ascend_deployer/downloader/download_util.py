#!/usr/bin/env python3
# coding: utf-8
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
import configparser
import ctypes
import hashlib
import json
import os
import platform
import socket
import ssl
import sys
import time
from urllib import request
from urllib.error import ContentTooShortError, URLError

try:
    from . import obs_downloader
except ImportError:
    pass
from . import logger_config


def get_download_path():
    """
    get download path
    """
    cur_dir = os.path.dirname(__file__)
    if 'site-packages' not in cur_dir and 'dist-packages' not in cur_dir:
        cur = os.path.dirname(cur_dir)
        return cur

    if platform.system() == 'Linux':
        deployer_home = os.getenv('HOME')
        if os.getenv('ASCEND_DEPLOYER_HOME') is not None:
            deployer_home = os.getenv('ASCEND_DEPLOYER_HOME')
    else:
        deployer_home = os.getcwd()

    return os.path.join(deployer_home, 'ascend-deployer')


LOG = logger_config.LOG
CUR_DIR = get_download_path()
ROOT_DIR = os.path.dirname(CUR_DIR)


class ConfigUtil:
    config_file = os.path.join(CUR_DIR, 'downloader/config.ini')

    def __init__(self) -> None:
        self.config = configparser.RawConfigParser()
        self.config.read(self.config_file)

    def get_pypi_url(self):
        return self.config.get('pypi', 'index_url')

    def get_proxy_verify(self):
        return self.config.getboolean('proxy', 'verify')

    def get_python_version(self):
        return self.config.get('python', 'ascend_python_version')

    def is_parallel_download(self):
        return str(self.config.get('download_config', 'parallel_download')).strip() == "1"


CONFIG_INST = ConfigUtil()


class ProxyUtil:
    def __init__(self) -> None:
        self.verify = CONFIG_INST.get_proxy_verify()
        self.proxy_handler = self._init_proxy_handler()
        self.https_handler = self._init_https_handler()

    @staticmethod
    def create_unverified_context():
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.verify_mode = ssl.CERT_NONE
        context.check_hostname = False
        return context

    @staticmethod
    def create_verified_context():
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        safe_ciphers = [
            'DHE-RSA-AES128-GCM-SHA256', 'DHE-RSA-AES256-GCM-SHA384', 'DHE-DSS-AES128-GCM-SHA256',
            'DHE-DSS-AES256-GCM-SHA384', 'DHE-PSK-CHACHA20-POLY1305', 'ECDHE-ECDSA-AES128-GCM-SHA256',
            'ECDHE-ECDSA-AES256-GCM-SHA384', 'ECDHE-RSA-AES128-GCM-SHA256', 'ECDHE-RSA-AES256-GCM-SHA384',
            'ECDHE-RSA-CHACHA20-POLY1305', 'ECDHE-PSK-CHACHA20-POLY1305', 'DHE-RSA-AES128-CCM',
            'DHE-RSA-AES256-CCM', 'DHE-RSA-AES128-CCM8', 'DHE-RSA-AES256-CCM8',
            'DHE-RSA-CHACHA20-POLY1305', 'PSK-AES128-CCM', 'PSK-AES256-CCM',
            'DHE-PSK-AES128-CCM', 'DHE-PSK-AES256-CCM', 'PSK-AES128-CCM8',
            'PSK-AES256-CCM8', 'DHE-PSK-AES128-CCM8', 'DHE-PSK-AES256-CCM8',
            'ECDHE-ECDSA-AES128-CCM', 'ECDHE-ECDSA-AES256-CCM', 'ECDHE-ECDSA-AES128-CCM8',
            'ECDHE-ECDSA-AES256-CCM8', 'ECDHE-ECDSA-CHACHA20-POLY1305']
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        context.set_ciphers(':'.join(safe_ciphers))
        return context

    @staticmethod
    def _init_proxy_handler():
        return request.ProxyHandler()

    def build_proxy_handler(self):
        opener = request.build_opener(self.proxy_handler,
                                      self.https_handler)
        opener.addheaders = [
            (
                "User-Agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
            )
        ]
        request.install_opener(opener)

    def _init_https_handler(self):
        if not self.verify:
            context = self.create_unverified_context()
        else:
            context = self.create_verified_context()

        return request.HTTPSHandler(context=context)


class DownloadError(Exception):
    def __init__(self, url, dst_file):
        self.url, self.dst_file = url, dst_file


class DownloadCheckError(Exception):
    def __init__(self, dst_file):
        self.dst_file = dst_file


class UrlOpenError(Exception):
    def __init__(self, msg):
        self.err_msg = msg


class PythonVersionError(Exception):
    def __init__(self, msg):
        self.err_msg = msg


class DownloadUtil:
    proxy_inst = ProxyUtil()
    start_time = time.time()

    @staticmethod
    def call_schedule(pkg, obs_check):
        def schedule(blocknum, blocksize, totalsize):
            try:
                speed = (blocknum * blocksize) / (time.time() - DownloadUtil.start_time)
            except ZeroDivisionError as err:
                print(err)
                LOG.error(err)
                raise
            if obs_check:
                try:
                    speed = blocknum * 1.0 / totalsize
                except ZeroDivisionError as err:
                    print(err)
                    LOG.error(err)
                    raise
            speed = float(speed) / 1024
            speed_str = r" {:.2f} KB/s".format(speed)
            if speed >= 1024:
                speed_str = r" {:.2f} MB/s".format(speed / 1024)
            recv_size = blocknum * blocksize
            # config scheduler
            f = sys.stdout
            pervent = recv_size / totalsize
            if obs_check:
                pervent = blocknum / blocksize
            if pervent > 1:
                pervent = 1
            percent_str = "{:.2f}%".format(pervent * 100)
            n = round(pervent * 30)
            s = ('=' * (n - 1) + '>').ljust(30, '-')
            if len(pkg) > 50:
                pkg_str = "".join(list(pkg)[:47]) + "..."
            elif len(pkg) < 50:
                pkg_str = "".join(list(pkg)) + (50 - len(pkg)) * ""
            else:
                pkg_str = pkg

            if pervent == 1:
                s = ('=' * n).ljust(30, '-')
            print_str = '\r' + Color.CLEAR + Color.info("start downloading ") \
                        + pkg_str.ljust(53, ' ') + ' ' \
                        + percent_str.ljust(7, ' ') + '[' + s + ']' + speed_str.ljust(20)
            f.write(print_str)
            f.flush()

        return schedule

    @classmethod
    def download(cls, url: str, dst_file_name: str, sha256: str = ""):
        parent_dir = os.path.dirname(dst_file_name)
        if not os.path.exists(parent_dir):
            LOG.info("mkdir : %s", os.path.basename(parent_dir))
            os.makedirs(parent_dir, mode=0o750, exist_ok=True)

        res = cls.download_with_retry(url, dst_file_name)
        if not res:
            print(url.ljust(60), 'download failed')
            LOG.error('download %s failed', url)
            raise DownloadError(url, dst_file_name)
        else:
            LOG.info('download %s successfully', url)
            return True

    @classmethod
    def use_obs(cls, file_url):
        if (
                "obs" in sys.modules
                and file_url.startswith(obs_downloader.OBS_URL_STARTING)
                and file_url.endswith(".zip")
        ):
            return True
        return False

    @classmethod
    def download_with_retry(cls, url: str, dst_file_name: str, retry_times=5):
        socket.setdefaulttimeout(20)
        for retry in range(1, retry_times + 1):
            try:
                LOG.info('downloading try: %s from %s', retry, url)
                delete_if_exist(dst_file_name)
                cls.proxy_inst.build_proxy_handler()
                DownloadUtil.start_time = time.time()
                pkg_name = url.split('/')[-1].split('#')[0]
                use_obs = cls.use_obs(url)
                if use_obs:
                    local_file, _ = obs_downloader.obs_urlretrieve(url, dst_file_name,
                                                                   cls.call_schedule(pkg_name, use_obs))
                else:
                    local_file, _ = request.urlretrieve(url, dst_file_name, cls.call_schedule(pkg_name, use_obs))
                return is_exists(local_file)
            except (ContentTooShortError, URLError, ssl.SSLError) as ex:
                print(ex)
                LOG.error(ex)
            except socket.timeout as timeout:
                socket.setdefaulttimeout(retry * 60)
                print(timeout)
                LOG.error(timeout)
            except ConnectionResetError as reset:
                print('connection reset by peer, retry...')
                LOG.error('connection reset by peer:{}, retry...'.format(reset))
            except Exception as ex:
                print('download failed, retry...')
                LOG.error('download failed with err:{}, retry...'.format(ex))
            finally:
                pass
            print('please wait for a moment...')
            LOG.info('please wait for a moment...')
            time.sleep(retry * 2)
        return False

    @classmethod
    def urlopen(cls, url: str, retry_times=5):
        for retry in [x + 1 for x in range(retry_times)]:
            try:
                cls.proxy_inst.build_proxy_handler()
                resp = request.urlopen(url)
                return resp
            except ContentTooShortError as ex:
                print(ex)
                LOG.error(ex)
            except URLError as err:
                print(err)
                LOG.error(err)
            except socket.timeout as timeout:
                socket.setdefaulttimeout(retry * 60)
                print(timeout)
                LOG.error(timeout)
            finally:
                pass
            print('please wait for a moment...')
            LOG.info('please wait for a moment...')
            time.sleep(retry * 2)
        return None

    @classmethod
    def download_to_tmp(cls, url: str, retry_times=5):
        for retry in [x + 1 for x in range(retry_times)]:
            try:
                cls.proxy_inst.build_proxy_handler()
                tmp_file, _ = request.urlretrieve(url)
                return tmp_file
            except ContentTooShortError as ex:
                print(ex)
                LOG.error(ex)
            except URLError as err:
                print(err)
                LOG.error(err)
            except socket.timeout as timeout:
                socket.setdefaulttimeout(retry * 60)
                print(timeout)
                LOG.error(timeout)
            finally:
                pass
            print('please wait for a moment...')
            LOG.info('please wait for a moment...')
            time.sleep(retry * 2)
        return False


DOWNLOAD_INST = DownloadUtil()
BLOCKSIZE = 1024 * 1024 * 100


def calc_sha256(file_path):
    hash_val = None
    if file_path is None or not os.path.exists(file_path):
        return hash_val
    with open(file_path, 'rb') as hash_file:
        sha256_obj = hashlib.sha256()
        buf = hash_file.read(BLOCKSIZE)
        while len(buf) > 0:
            sha256_obj.update(buf)
            buf = hash_file.read(BLOCKSIZE)
        hash_val = sha256_obj.hexdigest()
    return hash_val


def calc_md5(file_path):
    md5_val = None
    if file_path is None or not os.path.exists(file_path):
        return md5_val
    with open(file_path, 'rb') as md5_file:
        md5_obj = hashlib.md5()
        buf = md5_file.read(BLOCKSIZE)
        while len(buf) > 0:
            md5_obj.update(buf)
            buf = md5_file.read(BLOCKSIZE)
        hash_val = md5_obj.hexdigest()
    return hash_val


def get_specified_python():
    if os.environ.get("ASCEND_PYTHON_VERSION"):
        specified_python = os.environ.get("ASCEND_PYTHON_VERSION")
    else:
        specified_python = CONFIG_INST.get_python_version()
    resources_json = os.path.join(CUR_DIR, 'downloader', 'python_version.json')
    with open(resources_json, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        available_python_list = [item['filename'].rstrip('.tar.xz') for item in data]
        if specified_python not in available_python_list:
            tips = "ascend_python_version is not available, " \
                   "available Python-x.x.x is in 3.7.0~3.7.11 and 3.8.0~3.8.11 and 3.9.0~3.9.9"
            print(tips)
            LOG.error(tips)
            raise PythonVersionError(tips)
    return specified_python


def delete_if_exist(dst_file_name: str):
    if os.path.exists(dst_file_name):
        LOG.info('{} already exists'.format(os.path.basename(dst_file_name)))
        os.remove(dst_file_name)
        LOG.info('{} already deleted'.format(os.path.basename(dst_file_name)))


def is_exists(dst_file_name: str):
    if os.path.exists(dst_file_name):
        LOG.info('{} exists after downloading, success'.format(os.path.basename(dst_file_name)))
        return True
    else:
        print('[ERROR] {} not exists after downloading, failed'.format(os.path.basename(dst_file_name)))
        LOG.info('{} not exists after downloading, failed'.format(os.path.basename(dst_file_name)))
        return False


def get_arch(os_list):
    """
    根据os_list判断需要下载哪些架构的包
    """
    arm, x86 = 0, 0
    for os_item in os_list:
        if not arm and "aarch64" in os_item:
            arm = 1
        if not x86 and "x86_64" in os_item:
            x86 = 1
        if arm and x86:
            break

    if arm and not x86:
        arch = "aarch64"
    elif not arm and x86:
        arch = "x86_64"
    else:
        arch = ("x86_64", "aarch64")

    return arch


class CheckHash:
    @classmethod
    def check_hash(cls, dst_file, sha256):
        """
        check_hash
        校验下载文件的hash值与给定hash值是否相等

        :param dst_file: 下载文件文件
        :param sha256:  hash
        :return:
        """
        file_hash = calc_sha256(dst_file)
        return sha256 == file_hash

    @classmethod
    def check_download_hash(cls, dst_file, url_with_hash):
        """
        check_download_hash
        校验下载文件的hash值与url中的hash值是否相等

        :param dst_file: 下载文件文件
        :param url_with_hash:  带hash值的URL
        :return:
        """
        if 'sha256=' in url_with_hash:
            key_word = 'sha256='
            file_hash = calc_sha256(dst_file)
        else:
            key_word = 'md5='
            file_hash = calc_md5(dst_file)
        index_of_hash = str(url_with_hash).index(key_word) + len(key_word)
        target_hash = url_with_hash[index_of_hash:]
        return target_hash == file_hash


CH = CheckHash()


class State(object):
    NONE = 0
    EXIT = 1
    ASK = 2


class Color:
    RED = '\033[31m'
    BLUE = '\033[32m'
    END = '\033[0m'
    YELLOW = '\033[93m'
    CLEAR = '\033[K'

    @classmethod
    def info(cls, msg):
        return cls.BLUE + msg + cls.END

    @classmethod
    def warn(cls, msg):
        return cls.YELLOW + msg + cls.END

    @classmethod
    def error(cls, msg):
        return cls.RED + msg + cls.END


def get_free_space_b(folder):
    """
    get the free space of 'folder' in windows or linux
    :param folder:the path to get space
    :return:bites of space size
    """
    if platform.system().lower() == 'windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize
