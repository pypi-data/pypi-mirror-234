#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Huawei Technologies Co., Ltd
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from ansible.plugins.callback import CallbackBase

try:
    from __main__ import display
except ImportError:
    display = None


class CallbackModule(CallbackBase):
    def __int__(self, *args, **kwargs):
        if display and display.columns > 112:
            display.columns = 112
