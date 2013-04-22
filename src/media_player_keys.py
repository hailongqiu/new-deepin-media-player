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


from widget.keymap  import get_keyevent_name

class MediaPlayKeys(object):
    def __init__(self, this):
        print "MediaPlayKeys..."
        self.this = this
        self.__init_values()

    def __init_values(self):
        self.gui = self.this.gui
        self.gui.app.window.connect("key-press-event", self.app_window_key_press_event)
        self.keymap = {} # 快捷键.
        self.keymap["Escape"]  = self.this.key_quit_fullscreen
        self.keymap["Return"]  = self.this.fullscreen_function
        self.keymap["Space"]   = self.this.key_pause
        self.keymap["Shift + Return"] = self.this.key_concise_mode

    def app_window_key_press_event(self, widget, event):
        keyval_name = get_keyevent_name(event)
        print "name:", keyval_name
        if self.keymap.has_key(keyval_name):
            self.keymap[keyval_name]()


