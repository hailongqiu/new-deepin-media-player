#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013 Deepin, Inc.
#               2013 Hailong Qiu
#
# Author:     Hailong Qiu <356752238@qq.com>
# Maintainer: Hailong Qiu <356752238@qq.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
from mplayer.ini import Config
from widget.utils import add_sys_path

#
# 获取 gui_plugins 的绝对路径.
LOAD_SYS_PLUGINS = os.path.join(os.path.dirname(sys.argv[0]), "gui_plugins")
SYS_PLUGINS_PATH = os.path.abspath(LOAD_SYS_PLUGINS)

class LoadSysPlugins(object):
    def __init__(self):

        self.__init_values()
        self.__init_scan_dir()

    def __init_values(self):
        self.plugins_dict = {}

    def __init_scan_dir(self):
        for name in os.listdir(SYS_PLUGINS_PATH):
            new_path = os.path.join(SYS_PLUGINS_PATH, name)
            if os.path.isdir(new_path): # 判断是否为目录.
                self.__init_scan_file(new_path)

    def __init_scan_file(self, dir):
        config_path = os.path.join(dir, "config.ini")
        if os.path.exists(config_path):
            ini = Config(config_path)
            # 获取模块名.
            modules_include = ini.get("ldmp-gui", "include")
            modules_id      = ini.get("ldmp-gui", "id")
            modules_name    = ini.get("ldmp-gui", "name")
            if modules_include and modules_id:
                add_path = os.path.join(dir, "src")
                add_sys_path(add_path) 
                sys.path.append(add_path)
                try:
                    # 导入模块.
                    modual = __import__("gui_plugins.%s.%s" % (modules_id, modules_include), fromlist=["keywords"])
                    # 返回类名.
                    class_init = modual.return_plugin()
                    # 返回实例化的组件.
                    self.plugins_dict[modules_name] = class_init()
                except Exception, e:
                    print "load_gui_plugins[error]:", e

if __name__ == "__main__":
    load_sys_plugins = LoadSysPlugins()

