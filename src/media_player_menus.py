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

from user_guide import init_user_guide

class MediaPlayMenus(object):
    def __init__(self, this):
        self.this = this
        self.gui  = self.this.gui
        self.ldmp = self.this.ldmp
        self.menus = self.this.gui.play_menus
        # 初始化连接事件.
        self.menus.config_gui = self.this.config_gui
        self.menus.quit       = self.menu_quit
        self.menus.init_user_guide = init_user_guide
        #self.menus.title_root_menu.set_menu_item_sensitive_by_index(1, False)

    def menu_quit(self):
        self.ldmp.quit()
        self.gui.app.window.destroy()

