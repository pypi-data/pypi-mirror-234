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
import sys
import platform
from subprocess import PIPE, Popen, CalledProcessError, STDOUT

import utils

CURSOR_UPWARD = u'\u001b[1A'
MAX_LEN = 80


def process_run_cmd_and_check(*popenargs, **kwargs):
    process = Popen(*popenargs, **kwargs)
    process.communicate()
    ret_code = process.returncode
    if ret_code:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(ret_code, cmd)
    return 0


def prepare_install():
    prepare_sh = os.path.join(utils.ROOT_PATH, 'scripts', 'prepare.sh')
    process = Popen(["bash", prepare_sh], shell=False, env=os.environ, stderr=STDOUT, stdout=PIPE)

    sys.stdout.write("\n")  # prevents the first line from being overwritten
    for line in iter(process.stdout.readline, b''):
        line = line.decode('utf-8').strip()
        if line.startswith('[ERROR]'):
            pass
        elif len(line) <= MAX_LEN:
            line += (MAX_LEN - len(line)) * " "
        else:
            # if the line too long(> MAX_LEN), only print first (MAX_LEN -3) characters and '...'
            line = line[0:MAX_LEN - 4] + "..."
        sys.stdout.write(CURSOR_UPWARD)
        sys.stdout.write("\r" + line + "\n")

    process.wait()
    ret_code = process.returncode
    if ret_code:
        raise CalledProcessError(ret_code, ["ascend_deployer/scripts/prepare.sh"])
    return 0


def prompt(tip):
    sys.stdout.write(tip)
    sys.stdout.flush()
    if platform.system() == 'Windows':
        import msvcrt
        answer = msvcrt.getch().decode('utf-8')
        print(answer)
        return answer
    fd = sys.stdin.fileno()
    if not os.isatty(fd):  # handle pipe
        answer = sys.stdin.read().strip()
        print(answer)
        return answer
    import tty
    import termios
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON & ~termios.ECHO  # 设置lflag, 禁用标准输入和回显模式
    try:
        tty.setraw(fd)
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        answer = sys.stdin.read(1)
        print(answer)
        return answer
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def accept_eula():
    eula_file = 'eula_en.txt'
    if 'zh_CN' in os.environ.get('LANG', ''):
        eula_file = 'eula_cn.txt'
    eula_file_path = os.path.join(utils.ROOT_PATH, 'scripts', eula_file)
    with open(eula_file_path, 'rb') as f:
        print(f.read().decode('utf-8'))
    answer = prompt("Do you accept the EULA to use Ascend-deployer?[y/N]")
    return len(answer) == 1 and answer.lower() == 'y'


class AnsibleJob(object):
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file

    @staticmethod
    def get_inventory_file():
        return os.path.join(utils.ROOT_PATH, 'inventory_file')

    @staticmethod
    def handle_python_env(args):
        ascend_python_version = os.environ.get("ASCEND_PYTHON_VERSION")
        if not ascend_python_version:
            config_file = os.path.join(utils.ROOT_PATH, 'downloader', 'config.ini')
            try:
                import configparser
                cfp = configparser.ConfigParser()
            except ImportError:
                import ConfigParser
                cfp = ConfigParser.SafeConfigParser()
            cfp.read(config_file)
            ascend_python_version = cfp.get('python', 'ascend_python_version')
        version_list = utils.get_python_version_list()
        if ascend_python_version not in version_list:
            raise Exception("ASCEND_PYTHON_VERSION is not available, "
                            "available python version list is {}".format(version_list))
        version = ascend_python_version.replace('P', 'p').replace('-', '')
        args.extend([
            '-e', 'python_tar={}'.format(ascend_python_version),
            '-e', 'python_version={}'.format(version),
        ])
        install_path = os.path.expanduser('~/.local/{}'.format(version))
        os.environ['PATH'] = '{}/bin:{}'.format(install_path, os.environ.get('PATH', ''))
        os.environ['LD_LIBRARY_PATH'] = '{}/lib:{}'.format(install_path, os.environ.get('LD_LIBRARY_PATH', ''))

    def run_playbook(self, tags, no_copy=False, envs=None, ansible_args=None):
        args = self.build_args(envs)
        skip_tags = []
        if tags:
            if not isinstance(tags, list):
                tags = [tags]
            if 'all' in tags:
                tags[tags.index('all')] = 'whole'  # all is ansible reserved tag
            if no_copy:
                skip_tags.append('copy')
            else:
                tags.append('copy')
            args.extend(['--tags', ','.join(tags)])
            if skip_tags:
                args.extend(['--skip-tags', ','.join(skip_tags)])
        if ansible_args:
            args.extend(ansible_args)
        return process_run_cmd_and_check(args, shell=False, env=os.environ)

    def build_args(self, envs):
        inventory_file = self.get_inventory_file()
        args = ['ansible-playbook', '-i', inventory_file, self.yaml_file]
        if not envs:
            envs = {}
        self.handle_python_env(args)
        for k, v in envs.items():
            args.extend(['-e', '{}={}'.format(k, v)])
        return args

    def run_ansible(self, run_args):
        inventory_file = self.get_inventory_file()
        args = ['ansible', '-i', inventory_file]
        args.extend(run_args)
        return process_run_cmd_and_check(args, shell=False, env=os.environ)


process_path = os.path.join(utils.ROOT_PATH, 'playbooks', 'process')
process_install = AnsibleJob(os.path.join(process_path, 'process_install.yml')).run_playbook
process_scene = AnsibleJob(os.path.join(process_path, 'process_scene.yml')).run_playbook
process_patch = AnsibleJob(os.path.join(process_path, 'process_patch.yml')).run_playbook
process_patch_rollback = AnsibleJob(os.path.join(process_path, 'process_patch_rollback.yml')).run_playbook
process_test = AnsibleJob(os.path.join(process_path, 'process_test.yml')).run_playbook
process_check = AnsibleJob(os.path.join(process_path, 'process_check.yml')).run_playbook
process_clean = AnsibleJob(None).run_ansible
process_ls = AnsibleJob(os.path.join(utils.ROOT_PATH, 'playbooks', 'report.yaml')).run_playbook
process_hccn = AnsibleJob(os.path.join(utils.ROOT_PATH, 'playbooks', 'hccn.yaml')).run_playbook
