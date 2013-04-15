#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Hailong Qiu
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

from skin import app_theme
from dtk.ui.application  import Application
from widget.movie_paned  import Paned
from widget.movie_window import MovieWindow
from widget.playlistview import PlayListView
from toolbar      import ToolBar
from locales import _
import gtk

class GUI(object):
    '''Media Player GUI kernel code.核心界面代码'''
    def __init__(self):        
        '''application.'''
        self.app = Application(False)
        # application set.
        self.app.set_default_size(800, 500)
        # self.app.window.resize
        self.app.set_icon(app_theme.get_pixbuf("icon.ico"))
        self.app.set_skin_preview(app_theme.get_pixbuf("frame.png"))
        # set titlebar.
        self.app.add_titlebar(["theme", "menu", "max", "min", "close"],
                              app_theme.get_pixbuf("logo.png"),
                              _("Deepin Media Player"), " ", 
                              add_separator = False)
        #
        self.main_ali = gtk.Alignment()
        self.main_vbox = gtk.VBox()
        self.main_ali.add(self.main_vbox)
        self.main_ali.set(0, 0, 1.0, 1.0)
        self.main_ali.set_padding(0, 2, 2, 2)
        '''movie screen. 电影播放屏幕.'''
        # 播放屏幕和播放列表的HBOX.
        self.play_list_view = PlayListView()
        self.screen_paned = Paned()
        self.screen_frame = gtk.Alignment(0.0, 0.0, 1.0, 1.0)
        self.screen = gtk.DrawingArea()
        self.screen_frame.add(self.screen)
        self.top_toolbar = ToolBar()
        self.screen_paned.add_top_widget(self.top_toolbar.hbox_hframe)
        '''
        self.screen_paned.add_bottom_widget()
        '''
        #
        self.screen_frame_event = self.screen_paned
        self.screen_paned.screen = self.screen
        #
        self.screen_paned.add1(self.screen_frame)
        self.screen_paned.add2(self.play_list_view.play_list_vbox)
        #
        self.main_vbox.pack_start(self.screen_paned, True, True)
        #
        self.app.main_box.pack_start(self.main_ali, True, True)

    ################################################################################

    def not_in_system_widget(self):
        # 判断handle toolbar 是否显示出来了.
        return (not self.screen_paned.show_check and 
                not self.screen_paned.top_win_show_check and
                not self.screen_paned.bottom_win_show_check) 

    def set_paned_handle(self, event):
        if self.screen_paned.show_check and (0 <= event.x <= 7):
            if self.screen_paned.get_move_width() == 0:
                self.screen_paned.set_move_width(self.screen_paned.save_move_width)
                self.screen_paned.set_all_size()
            else:
                self.screen_paned.set_jmp_end()
                self.screen_paned.set_all_size()


