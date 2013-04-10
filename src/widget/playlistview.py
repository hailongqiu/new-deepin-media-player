#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 ~ 2013 Deepin, Inc.
#               2012 ~ 2013 Hailong Qiu
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


from dtk.ui.scrolled_window import ScrolledWindow
from listview import ListView
from listview_base import Text
import gtk

class PlayListView(object):
    def __init__(self):
        self.play_list_vbox = gtk.VBox()
        self.scroll_win   = ScrolledWindow(0, 0)
        #self.scroll_win   = gtk.ScrolledWindow()
        self.scroll_win.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        self.list_view    = ListView()
        #
        self.list_view.on_draw_sub_item     =  self.__listview_on_draw_sub_item
        self.list_view.columns.add_range(["filename", "time"])
        self.list_view.columns[0].width = 100
        self.list_view.columns[1].width = 75
        #
        self.scroll_win.add_with_viewport(self.list_view)
        self.play_list_vbox.pack_start(gtk.Button("网络列表"), False, False)
        self.play_list_vbox.pack_start(self.scroll_win, True, True)
        #
        #
        for i in range(1, 200):
            self.list_view.items.add([str(i) + "楚汉传奇+", "12:12:12"])

    def __listview_on_draw_sub_item(self, e):
        if e.double_items == e.item:
            e.text_color = "#0000FF"
            text_size=9
            e.cr.set_source_rgba(0, 0, 0, 0.5)
            e.cr.rectangle(e.x, e.y, e.w, e.h)
            e.cr.fill()
        elif e.item in e.single_items:
            e.text_color = "#00FF00"
            text_size=9
            e.cr.set_source_rgba(0, 0, 0, 0.5)
            e.cr.rectangle(e.x, e.y, e.w, e.h)
            e.cr.fill()
        elif e.motion_items == e.item:
            e.text_color  = "#FF0000"
            text_size=9
            e.cr.set_source_rgba(0, 0, 0, 0.5)
            e.cr.rectangle(e.x, e.y, e.w, e.h)
            e.cr.fill()
        else:
            e.text_color = "#FFFFFF"
            text_size=9
        text = e.text.decode("utf-8")
         
        if len(text) > 8: 
            text = text[0:8] + "..."
        e.draw_text(e.cr, 
                str(text), 
                  e.x + 10, e.y, e.w, e.h,
                  text_color=e.text_color, 
                  text_size=text_size,
                  alignment=Text.LEFT)




