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
import csv
import os.path
import sys


def solve_value_list(value_list):
    res_iter = (item.get("name", "") + ":" + item.get("version", "") for item in value_list if isinstance(item, dict))
    return "\n".join(res_iter)


def get_hccn(hccn_list):
    if not hccn_list:
        return 'NA'
    for hccn in hccn_list:
        if isinstance(hccn, str) and 'success' not in hccn.lower():
            return 'fail'
    return 'ok'


def main(path):
    with open(path) as f:
        data = json.load(f)
        dir_name = os.path.dirname(path)
        ips = list(data.keys())

        fieldsname = ["IP", "node name", "node type", "node status", "npu", "packages", "HCCN health check", "ok pods",
                      "MindX-DL status"]
        flags = os.O_WRONLY | os.O_CREAT
        with os.fdopen(os.open(dir_name + '/report.csv', flags, 0o644), 'w', newline='') as wf:
            writer = csv.DictWriter(wf, fieldnames=fieldsname)
            writer.writeheader()
            for ip in ips:
                row = [ip]
                npu = data.get(ip, {}).get('npu', 'NA')
                packages = solve_value_list(data.get(ip, {}).get('packages', []))
                hccn_list = data.get(ip, {}).get('hccn', [])
                hccn_info = get_hccn(hccn_list)
                node_name = data.get(ip, {}).get('node name', 'NA')
                node_type = data.get(ip, {}).get('node type', 'NA')
                status = data.get(ip, {}).get('status', 'NA')
                ready_pods = "\n".join(data.get(ip, {}).get('ready pods', []))
                result = data.get(ip, {}).get('dl result', 'NA')
                row.extend(
                    [node_name, node_type, status, npu, packages or 'NA', hccn_info, ready_pods or 'NA',
                     result or 'NA'])
                writer.writerow(dict(zip(fieldsname, row)))


if __name__ == '__main__':
    main(sys.argv[1])
