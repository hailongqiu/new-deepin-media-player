#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
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


import gtk

class GuiPlayList(object):
    def __init__(self):
        self.play_list = gtk.Button("播放列表")
     		  
    def init_values(self, this): # 初始化传过来的变量.
        self.gui = this.gui
        self.ldmp = this.ldmp
        print self.gui
        print self.ldmp
    
    def auto(self): # 是否自动运行插件. True 自动 False 不自动
        return True
		  
    def start(self): # 开启插件.
        self.gui.screen_and_play_list_hbox.pack_start(self.play_list, False, False)
        self.gui.screen_and_play_list_hbox.show_all()
        print "start plugin..."
		  
    def stop(self): # 关闭插件.
        if len(self.gui.screen_and_play_list_hbox.get_children()) >= 2:
            self.gui.screen_and_play_list_hbox.remove(self.play_list)
            print "stop plugin..."
	  
def return_plugin(): 
    return GuiPlayList # 需要返回的类名.
