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
import os
import re
import json
import stat
import argparse
import getpass
import logging
import logging.handlers
import platform
import shutil

ROOT_PATH = SRC_PATH = os.path.dirname(__file__)
MODE_700 = stat.S_IRWXU
MODE_600 = stat.S_IRUSR | stat.S_IWUSR
MODE_400 = stat.S_IRUSR

dir_list = ['downloader', 'playbooks', 'tools', 'ansible_plugin', 'group_vars', 'patch', 'scripts', 'yamls']
file_list = ['install.sh', 'inventory_file', 'ansible.cfg',
             '__init__.py', 'ascend_deployer.py', 'jobs.py', 'utils.py',
             'version.json']


def copy_scripts():
    """
    copy scripts from library to ASCEND_DEPLOY_HOME
    the default ASCEND_DEPLOYER_HOME is HOME
    """
    if SRC_PATH == ROOT_PATH:
        return

    if not os.path.exists(ROOT_PATH):
        os.makedirs(ROOT_PATH, mode=0o750, exist_ok=True)
    for dir_name in dir_list:
        src = os.path.join(SRC_PATH, dir_name)
        dst = os.path.join(ROOT_PATH, dir_name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copytree(src, dst)

    for filename in file_list:
        src = os.path.join(SRC_PATH, filename)
        dst = os.path.join(ROOT_PATH, filename)
        if not os.path.exists(dst) and os.path.exists(src):
            shutil.copy(src, dst)


if 'site-packages' in ROOT_PATH or 'dist-packages' in ROOT_PATH:
    deployer_home = os.getcwd()
    if platform.system() == 'Linux':
        deployer_home = os.getenv('ASCEND_DEPLOYER_HOME', os.getenv('HOME'))
    ROOT_PATH = os.path.join(deployer_home, 'ascend-deployer')
    copy_scripts()


class ValidChoices(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, list(set(values)))


def pretty_format(text):
    results = []
    loc = text.index(':') + 1
    results.append(text[:loc])
    results.extend(text[loc:].split(','))
    return results


class HelpFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if ':' in text:
            return pretty_format(text)
        import textwrap
        return textwrap.wrap(text, width, break_on_hyphens=False)


def args_with_comma(args):
    new_args = []
    for arg in args:
        sep_loc = arg.find('=')
        ver_loc = arg.find('==')
        if sep_loc > 0 and sep_loc != ver_loc:
            new_args.append(arg[:sep_loc])
            arg = arg[sep_loc + 1:]
        for sub_arg in arg.split(','):
            if sub_arg:
                new_args.append(sub_arg)
    return new_args


os_items = sorted(os.listdir(os.path.join(ROOT_PATH, "downloader", "config")))
pkg_file_list = os.listdir(os.path.join(ROOT_PATH, "downloader", "software"))
pkg_items = set()
for pkg_file in pkg_file_list:
    pkg_name, version = pkg_file.split('_')
    pkg_items.add(pkg_name)
    pkg_items.add('{}=={}'.format(pkg_name, version.replace('.json', '')))
pkg_items = sorted(pkg_items)


def get_python_version_list():
    python_version_json = os.path.join(ROOT_PATH, 'downloader', 'python_version.json')
    with open(python_version_json, 'r') as json_file:
        data = json.load(json_file)
        available_python_list = [item['filename'].rstrip('.tar.xz') for item in data]
        return available_python_list


def get_name_list(dir_path, prefix, suffix):
    items = []
    for file_name in os.listdir(dir_path):
        if file_name.startswith(prefix) and file_name.endswith(suffix):
            item = file_name.replace(prefix, '').replace(suffix, '')
            items.append(item)
    return sorted(items)


install_items = get_name_list(os.path.join(ROOT_PATH, "playbooks", "install"), 'install_', '.yml')
scene_items = get_name_list(os.path.join(ROOT_PATH, "playbooks", "scene"), 'scene_', '.yml')
patch_items = get_name_list(os.path.join(ROOT_PATH, "playbooks", "install", "patch"), "install_", ".yml")
test_items = get_name_list(os.path.join(ROOT_PATH, "playbooks", "test"), "test_", ".yml")

LOG_MAX_BACKUP_COUNT = 5
LOG_MAX_SIZE = 20 * 1024 * 1024
LOG_FILE = os.path.join(ROOT_PATH, 'install.log')
LOG_OPERATION_FILE = os.path.join(ROOT_PATH, 'install_operation.log')


class UserHostFilter(logging.Filter):
    user = getpass.getuser()
    host = os.getenv('SSH_CLIENT', 'localhost').split()[0]

    def filter(self, record):
        record.user = self.user
        record.host = self.host
        return True


class RotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self):
        try:
            os.chmod(self.baseFilename, mode=0o400)
        except PermissionError:
            os.chmod('{}.{}'.format(self.baseFilename, LOG_MAX_BACKUP_COUNT), mode=0o600)
        finally:
            logging.handlers.RotatingFileHandler.doRollover(self)
            os.chmod(self.baseFilename, mode=0o600)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        'extra': {
            'format': "%(asctime)s %(user)s@%(host)s [%(levelname)s] "
                      "[%(filename)s:%(lineno)d %(funcName)s] %(message)s"
        }
    },
    "filters": {
        "user_host": {
            '()': UserHostFilter
        }
    },
    "handlers": {
        "install": {
            "level": "INFO",
            "formatter": "extra",
            "class": 'utils.RotatingFileHandler',
            "filename": LOG_FILE,
            'maxBytes': LOG_MAX_SIZE,
            'backupCount': LOG_MAX_BACKUP_COUNT,
            'encoding': "UTF-8"
        },
        "install_operation": {
            "level": "INFO",
            "formatter": "extra",
            "class": 'utils.RotatingFileHandler',
            "filename": LOG_OPERATION_FILE,
            'maxBytes': LOG_MAX_SIZE,
            'backupCount': LOG_MAX_BACKUP_COUNT,
            'encoding': "UTF-8"
        },
    },
    "loggers": {
        "install": {
            "handlers": ["install"],
            "level": "INFO",
            "propagate": False,
            "filters": ["user_host"]
        },
        "install_operation": {
            "handlers": ["install_operation"],
            "level": "INFO",
            "propagate": False,
            "filters": ["user_host"]
        },
    }
}


def ignore_permission(dir_path, name):
    return dir_path.endswith('__pycache__') or \
        name.startswith(('__pycache__', '.git'))


def update_folder_permission(dir_path, dir_name):
    if ignore_permission(dir_path, dir_name):
        return
    os.chmod(os.path.join(dir_path, dir_name), MODE_700)


def update_file_permission(dir_path, file_name):
    if ignore_permission(dir_path, file_name):
        return
    if file_name.endswith(('.log', '.ini', '.cfg', '.json', '.yml', '.yaml',
                           '.txt', 'inventory_file')):
        mode = MODE_600
    elif re.search(r'\.log\.\d{1,2}$', file_name):
        mode = MODE_400
    else:
        mode = MODE_700
    os.chmod(os.path.join(dir_path, file_name), mode)


def update_permissions():
    for base, dirs, files in os.walk(ROOT_PATH):
        for dir_name in dirs:
            update_folder_permission(base, dir_name)
        for file_name in files:
            update_file_permission(base, file_name)
