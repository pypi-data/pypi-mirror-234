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
import json
import os
import sys
import yaml

EOL_MSG = "[ASCEND] The lifecycle of {} is over and is no longer supported"
SUPPORT_MSG = "[ASCEND] {} has no support for {}"


class ChainDict(dict):
    def __getattr__(self, item):
        if item in self:
            value = self[item]
            if isinstance(value, dict):
                return ChainDict(value)
            return value
        return ChainDict()

    def __getitem__(self, item):
        if item in self:
            return super(ChainDict, self).__getitem__(item)
        return ChainDict()


class CompatibilityCheck(object):

    def __init__(self, fact_path, host, tags):
        self.fact_path = fact_path
        self.host = host
        self.tags = tags.split(',') if isinstance(tags, str) else []
        self.tags = list(set(self.tags))
        if 'all' in self.tags:
            self.tags.remove('all')  # ignore ansible reserved tag
        base_dir = os.path.dirname(os.path.dirname(__file__))
        config_file = os.path.join(
            base_dir, 'playbooks', 'roles', 'mindx.check',
            'defaults', 'compatibility_map.yml')
        with open(config_file) as f:
            docs = yaml.safe_load(f)
            self.config = ChainDict(docs)
        self.fact_info = ChainDict()

    @staticmethod
    def record_error(msg):
        raise Exception(msg)

    @classmethod
    def run(cls):
        try:
            fact_path, host, tags = sys.argv[1:]
        except ValueError:
            print("invalid param size")
            sys.exit(-1)
        c = cls(fact_path, host, tags)
        try:
            c.check_host()
        except TypeError:
            print("not found needed data")
            sys.exit(-1)
        except Exception as e:
            print(e)
            sys.exit(-1)

    def check_host(self):
        if not os.path.exists(self.fact_path):
            raise Exception("fact_path not exist")
        host_fact_file = os.path.join(self.fact_path, self.host)
        with open(host_fact_file) as f:
            content = json.load(f)
        self.fact_info = ChainDict(content)
        self.check_card()
        self.check_model()
        self.check_os()

    def check_card(self):
        card = self.fact_info.ansible_local.npu_info.card
        os_and_arch = self.fact_info.os_and_arch
        if card in self.config.eol_card:
            self.record_error(EOL_MSG.format(card))
        support_os_arch_list = self.config.card_dict[card]
        if support_os_arch_list and os_and_arch not in support_os_arch_list:
            self.record_error(SUPPORT_MSG.format(card, os_and_arch))

    def check_model(self):
        model = self.fact_info.ansible_local.npu_info.model
        if model in self.config.eol_model:
            self.record_error(EOL_MSG.format(model))
        unsupported_tags = self.config.model_tags_not_support[model]
        for tag in self.tags:
            if tag in unsupported_tags:
                self.record_error(SUPPORT_MSG.format(tag, model))

    def check_os(self):
        os_and_arch = self.fact_info.os_and_arch
        supported_tags = self.config.os_arch_tags_support[os_and_arch]
        for tag in self.tags:
            if tag not in supported_tags:
                self.record_error(SUPPORT_MSG.format(tag, os_and_arch))


if __name__ == '__main__':
    CompatibilityCheck.run()
