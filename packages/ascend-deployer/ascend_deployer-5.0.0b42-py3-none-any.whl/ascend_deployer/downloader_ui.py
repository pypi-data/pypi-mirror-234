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
"""gui application using tk"""
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

import ascend_download
from downloader.software_mgr import SoftwareMgr
from downloader.download_util import State
from utils import os_items, pkg_items


class Win(object):
    """
    downloader ui window
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('离线安装下载器')
        self.root.geometry('620x480')
        self.root.resizable(False, False)
        self.root.protocol('WM_DELETE_WINDOW', self.root.destroy)
        self.os_dict = {}
        self.pkg_dict = {}
        self.os_list = []
        self.pkg_list = []
        self.combo_list = []
        self.software_mgr = SoftwareMgr()
        self.init()
        self.layout()

    def layout(self):
        frame_left = self.create_frame("OS_LIST", 0, True)
        frame_right = self.create_frame("PKG_LIST", 2, False)
        frame_middle = tk.LabelFrame(
            tk.Button(self.root, text="开始下载").grid(row=0, column=1)
        )
        frame_middle.grid(row=0, column=1, padx=5)
        tk.Button(frame_left, text="全选",
                  command=self.select_all_os).grid(row=0, column=0, sticky='w')
        tk.Button(frame_left, text="全不选",
                  command=self.unselect_all_os).grid(row=0, column=0)
        tk.Button(frame_right, text="清空",
                  command=self.unselect_all_pkg).grid(row=0, column=0, sticky='w')
        tk.Button(frame_middle, text='开始下载',
                  command=self.start_download).pack()
        os_idx = 0
        for os_name, var in sorted(self.os_dict.items()):
            os_idx += 1
            tk.Checkbutton(frame_left, width=30, text=os_name,
                           variable=var, anchor='w').grid(row=os_idx,
                                                          column=0)

        for i, name in enumerate(sorted(self.pkg_dict.keys())):
            tk.Label(frame_right, text=name).grid(row=i + 1, sticky='W')
            combo = ttk.Combobox(frame_right, textvariable=tk.StringVar(), state='readonly')
            combo['value'] = self.pkg_dict.get(name, [])
            combo.grid(row=i + 1, sticky='W', padx=80, pady=5)
            self.combo_list.append([name, combo])

    def run(self):
        """
        the main loop of the window
        """
        self.root.mainloop()

    def start_download(self):
        """
        start downloading, the window will exit
        """
        self.refresh_data()
        check_stat, msg = self.software_mgr.check_selected_software(self.os_list, self.pkg_list)
        if not self.os_list:
            tkinter.messagebox.showwarning(title="Warning", message="os_list必须勾选")
        elif check_stat == State.EXIT:
            tkinter.messagebox.showwarning(title="Warning", message=msg)
        elif check_stat == State.ASK:
            if tkinter.messagebox.askyesnocancel(title="Warning",
                                                 message=msg[0].upper() + msg[1:] + "need to force download or not?"):
                self.work()
        else:
            self.work()

    def init(self):
        """
        init os_dict and pkg_dict
        """
        for os_name in os_items:
            var = tk.IntVar()
            var.set(0)
            self.os_dict[os_name] = var
        for pkg_name in pkg_items:
            if '=' not in pkg_name:
                continue
            name, version = pkg_name.split('==')
            self.pkg_dict.setdefault(name, []).append(version)

    def refresh_data(self):
        """
        refresh os_list and pkg_list
        """
        self.os_list.clear()
        for os_name, var in sorted(self.os_dict.items()):
            if var.get() == 1:
                self.os_list.append(os_name)

        self.pkg_list.clear()
        for name, combo in self.combo_list:
            if combo.get() != "":
                self.pkg_list.append('{}=={}'.format(name, combo.get()))

    def select_all_os(self):
        for item in os_items:
            self.os_dict.get(item).set(1)

    def unselect_all_os(self):
        for item in os_items:
            self.os_dict.get(item).set(0)

    def unselect_all_pkg(self):
        for _, combo in self.combo_list:
            combo.set('')

    def create_frame(self, text, column, scroll):
        box = tk.LabelFrame(self.root, text=text)
        box.grid(row=0, column=column)
        canvas = tk.Canvas(box)
        canvas.pack(side='left', fill="both", expand=True)
        frame = tk.Frame(canvas)
        scrollbar = tk.Scrollbar(box, orient="vertical", command=canvas.yview)
        canvas.configure(
            yscrollcommand=scrollbar.set, width=250, height=450
        )
        if scroll:
            scrollbar.pack(side='left', fill="y")

        def on_frame_configure(_):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)
        canvas.create_window((4, 4), window=frame, anchor="nw", tags="frame")
        return frame

    def work(self):
        self.root.destroy()
        arg_list = ['--os-list', ','.join(self.os_list)] + (
            ['--download', ','.join(self.pkg_list)] if self.pkg_list else [])
        ascend_download.main(
            args=arg_list,
            check=False
        )


def win_main():
    """
    start gui application
    """
    app = Win()
    app.run()


if __name__ == '__main__':
    win_main()
