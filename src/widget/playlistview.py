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


from dtk.ui.theme import ui_theme
from dtk.ui.scrolled_window import ScrolledWindow
from dtk.ui.draw import draw_vlinear
from listview import ListView
from listview_base import Text
from color import alpha_color_hex_to_cairo, color_hex_to_cairo
import gtk

class PlayListView(object):
    def __init__(self):
        self.listview_color = ui_theme.get_color("scrolledbar")
        self.play_list_vbox = gtk.VBox()
        self.scroll_win   = ScrolledWindow(0, 0)
        self.scroll_win.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        self.list_view    = ListView()
        #
        self.list_view.on_draw_sub_item =  self.__listview_on_draw_sub_item
        self.list_view.columns.add_range(["filename", "time"])
        self.list_view.columns[0].width = 100
        self.list_view.columns[1].width = 75
        #
        self.scroll_win.add_with_viewport(self.list_view)
        #self.play_list_vbox.pack_start(gtk.Button("网络列表"), False, False)
        self.play_list_vbox.pack_start(self.scroll_win, True, True)
        #
        #
        for path in [
                    "/home/long/视频/test.mp4",
                    "/home/long/视频/test3.mkv",
                    "/home/long/视频/test2.rmvb",
                    "/home/long/视频/test3.mkv",
                    "/home/long/视频/test4.mkv",
                    "/home/long/视频/test.mp4",
                    ]:
            self.list_view.items.add([path, "12:12:12", path])
        # 网络电视测试.
        net_uri = "mms://112.230.192.196/zb10"
        self.list_view.items.add(["网络电视:体育频道", "12:12:12", net_uri])
        net_uri = "mms://mediasrv2.iptv.xmg.com.cn/tvyingshi"        
        self.list_view.items.add(["XXX卫视", "12:12:12", net_uri])
        net_uri = "http://f.youku.com/player/getFlvPath/sid/00_00/st/flv/fileid/03000201004F146D1FB1970001F869843C93CE-5F43-F826-92C4-B586DDD30EE1?K=19fe5a7e7d8cf681282888df"
        self.list_view.items.add(["王心凌", "12:12:12", net_uri])
        net_uri = "http://f.youku.com/player/getFlvPath/sid/00_00/st/flv/fileid/0300020500516670A5831606257BB606FC8A83-4EED-04FD-5E13-0D1DBCA204F1?K=9d51747487369aa9261cf402"
        self.list_view.items.add(["嘻哈高手", "12:12:12", net_uri])
        net_uri = "http://f.youku.com/player/getFlvPath/sid/00_00/st/flv/fileid/0300020700515165A330C803BAF2B136BE57BF-061D-C2AC-F017-EC6944CFBD7E?K=70f0f7ce662b0d9d24115f3b"
        self.list_view.items.add(["弓箭手", "12:12:12", net_uri])


    def __listview_on_draw_sub_item(self, e):
        color = self.listview_color.get_color()
        if e.double_items == e.item:
            e.text_color = "#000000"
            text_size=9
            color_info = [(0, (color, 0.8)), (1, (color, 0.8))] 
            draw_vlinear(e.cr,
                         e.x, e.y, e.w, e.h,
                         color_info
                         )
        elif e.item in e.single_items:
            e.text_color = "#FFFFFF"
            text_size=9
            color_info = [(0, (color, 0.5)), (1, (color, 0.5))] 
            draw_vlinear(e.cr,
                         e.x, e.y,
                         e.w, e.h,
                         color_info
                         )
        elif e.motion_items == e.item:
            e.text_color  = "#FFFFFF"
            text_size=9
            color_info = [(0, (color, 0.2)), (1, (color, 0.2))] 
            draw_vlinear(e.cr,
                         e.x, e.y,
                         e.w, e.h,
                         color_info
                         )
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




