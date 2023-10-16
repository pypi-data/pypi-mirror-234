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
import argparse
import logging
import logging.config
from functools import wraps

import utils

LOG = logging.getLogger('install')
LOG_OP = logging.getLogger('install_operation')


def add_log(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        cmd = ' '.join(sys.argv[1:])
        dl_scene = False
        if 'dl' in cmd:  # only for support XX ugly implementation
            dl_scene = True
        reason = ''
        try:
            result = f(*args, **kwargs)
            if dl_scene:
                LOG.info("[INFO] Ascend DL deployed success --ascend-deployer")
            return result
        except SystemExit as e:
            if e.code == 0:
                return 0
            reason = 'exit code: {}'.format(e.code)
            return -1
        except KeyboardInterrupt:  # handle KeyboardInterrupt
            reason = "User interrupted the program by Keyboard"
            return -1
        except BaseException as e:  # handle other exceptions
            reason = str(e)
            return -1
        finally:
            msg = "run cmd: {} successfully".format(cmd)
            if reason:
                msg = "run cmd: {} failed, reason: {}".format(cmd, reason)
            print(msg)
            if dl_scene and reason:
                LOG.error("[ERROR]Ascend DL deployed failed --ascend-deployer")
            if reason:
                LOG_OP.error(msg)
            else:
                LOG_OP.info(msg)

    return wrap


class CLI(object):
    def __init__(self, prog, desc, epilog=None):
        self.parser = argparse.ArgumentParser(
            prog=prog, description=desc, epilog=epilog, formatter_class=utils.HelpFormatter)
        self.parser.add_argument("--check", dest="check", action="store_true", default=False, help="check environment")
        self.parser.add_argument("--clean", dest="clean", action="store_true", default=False,
                                 help="clean resources on remote servers")
        self.parser.add_argument("--nocopy", dest="no_copy", action="store_true", default=False,
                                 help="do not copy resources to remote servers when install for remote")
        self.parser.add_argument("--force_upgrade_npu", dest="force_upgrade_npu", action="store_true", default=False,
                                 help="can force upgrade NPU when not all devices have exception")
        self.parser.add_argument("--verbose", dest="verbose", action="store_true", default=False, help="Print verbose")
        self.parser.add_argument("--ls", dest="ls", action="store_true", default=False,
                                 help="Show all packages version")
        self.parser.add_argument("--install", dest="install", nargs="+", choices=utils.install_items,
                                 action=utils.ValidChoices,
                                 metavar="<package_name>", help="Install specific package: %(choices)s")
        self.parser.add_argument("--stdout_callback", dest="stdout_callback",
                                 help="set display plugin, e.g. ansible_log")
        self.parser.add_argument("--install-scene", dest="scene", nargs="?", choices=utils.scene_items,
                                 metavar="<scene_name>", help="Install specific scene: %(choices)s")
        self.parser.add_argument("--patch", dest="patch", nargs="+", choices=utils.patch_items,
                                 action=utils.ValidChoices,
                                 metavar="<package_name>", help="Patching specific package: %(choices)s")
        self.parser.add_argument("--patch-rollback", dest="patch_rollback", nargs="+", choices=utils.patch_items,
                                 action=utils.ValidChoices,
                                 metavar="<package_name>", help="Rollback specific package: %(choices)s")
        self.parser.add_argument("--test", dest="test", nargs="+", choices=utils.test_items, metavar="<target>",
                                 action=utils.ValidChoices,
                                 help="test the functions: %(choices)s")
        self.parser.add_argument("--hccn", dest="hccn", action="store_true", default=False,
                                 help="Setting hccn")

    @add_log
    def run(self):
        args = self.parser.parse_args(utils.args_with_comma(sys.argv[1:]))
        if not any([args.install, args.scene, args.patch, args.patch_rollback, args.test, args.check, args.clean,
                    args.ls, args.hccn]):
            self.parser.print_help()
            raise Exception("expected one valid argument at least")
        if args.install and args.scene:
            raise Exception("Unsupported --install and --install-scene at same time")

        if args.stdout_callback:
            os.environ['ANSIBLE_STDOUT_CALLBACK'] = args.stdout_callback
        os.environ['ANSIBLE_CACHE_PLUGIN_CONNECTION'] = os.path.join(utils.ROOT_PATH, 'facts_cache')
        os.environ['ANSIBLE_CONFIG'] = os.path.join(utils.ROOT_PATH, 'ansible.cfg')

        import jobs
        if any([args.install, args.scene, args.patch]) and not args.check:
            if not jobs.accept_eula():
                LOG_OP.error('reject EULA, quit to install')
                raise Exception('reject EULA, quit to install')
            LOG_OP.info("accept EULA, start to install")
        jobs.prepare_install()
        ansible_args = ['-v'] if args.verbose else []
        if args.check:
            check_tags = args.install if args.install else []
            if args.scene:
                check_tags.append(args.scene)
            return jobs.process_check(check_tags, no_copy=True, ansible_args=ansible_args)
        for handler, tags in (
                (jobs.process_install, args.install),
                (jobs.process_scene, args.scene),
                (jobs.process_patch, args.patch),
                (jobs.process_patch_rollback, args.patch_rollback)):
            if not tags:
                continue
            envs = {
                'hosts_name': 'worker',
                'force_upgrade_npu': 'true' if args.force_upgrade_npu else 'false',
                'do_upgrade': 'true',
            }
            return handler(tags, no_copy=args.no_copy, envs=envs, ansible_args=ansible_args)
        if args.test:
            envs = {'hosts_name': 'worker'}
            return jobs.process_test(args.test, envs=envs, ansible_args=ansible_args)
        if args.clean:
            run_args = ['worker', '-m', 'shell', '-a', 'rm -rf ~/resources.tar ~/resources']
            run_args.extend(ansible_args)
            return jobs.process_clean(run_args)
        if args.ls:
            envs = {'only_package': 'true'}
            return jobs.process_ls(None, envs=envs, ansible_args=ansible_args)
        if args.hccn:
            return jobs.process_hccn(None, ansible_args=ansible_args)


def main():
    logging.config.dictConfig(utils.LOGGING_CONFIG)
    utils.update_permissions()
    cli = CLI(
        "ascend-deployer",
        "Manage Ascend Packages and dependence packages for specified OS"
    )
    return cli.run()


if __name__ == '__main__':
    sys.exit(main())
