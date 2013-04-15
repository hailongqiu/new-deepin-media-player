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
from dtk.ui.skin_config  import skin_config
from dtk.ui.application  import Application
from widget.movie_paned  import Paned
from widget.movie_window import MovieWindow
from widget.playlistview import PlayListView
from widget.toolbar      import ToolBar
from widget.draw         import draw_pixbuf
from widget.color        import alpha_color_hex_to_cairo
from widget.bottom_toolbar import BottomToolBar
from locales import _
import gtk

class GUI(object):
    '''Media Player GUI kernel code.核心界面代码'''
    def __init__(self):        
        '''application.'''
        self.__init_values()
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
        self.screen_paned.paint_bottom_window = self.__paint_bottom_toolbar_background
        self.screen_frame = gtk.Alignment(0.0, 0.0, 1.0, 1.0)
        self.screen = gtk.DrawingArea()
        self.screen_frame.add(self.screen)
        self.top_toolbar = ToolBar()
        self.bottom_toolbar = BottomToolBar()
        self.screen_paned.add_top_widget(self.top_toolbar.hbox_hframe)
        self.screen_paned.add_bottom_widget(self.bottom_toolbar.vbox)
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

    def __init_values(self):
        self.child2_show_check = True # True 显示 False 隐藏

    ################################################################################
    ##
    def __paint_bottom_toolbar_background(self, e):
        # 将皮肤的图片画在bottom toolbar上,作为背景.
        cr = e.window.cairo_create()
        bottom_size = e.window.get_size()
        # draw background.
        cr.set_source_rgba(*alpha_color_hex_to_cairo(("#ebebeb", 0.1)))
        cr.rectangle(0, 0, bottom_size[0], bottom_size[1])
        cr.fill()
        # draw background pixbuf.
        pixbuf = skin_config.background_pixbuf
        app_h = self.app.window.allocation.height
        app_w = self.app.window.allocation.width
        bottom_h = bottom_size[1]
        # 当图片的高度小雨窗口高度的时候,只拿出图片的最尾巴.
        if pixbuf.get_height() > app_h + bottom_h:
            h = app_h
        else:
            h = pixbuf.get_height() - bottom_h
        # 当图片小于窗口宽度的时候,拉伸图片.
        if pixbuf.get_width() < app_w:
            pixbuf = pixbuf.scale_simple(app_w,
                                pixbuf.get_width(),
                                gtk.gdk.INTERP_BILINEAR)

        draw_pixbuf(cr, 
                    pixbuf, 
                    0, 
                    -(h))

    def not_in_system_widget(self):
        # 判断handle toolbar 是否显示出来了.
        return (not self.screen_paned.show_check and 
                not self.screen_paned.top_win_show_check and
                not self.screen_paned.bottom_win_show_check) 

    def set_paned_handle(self, event):
        if self.screen_paned.show_check and (0 <= event.x <= 7):
            self.child2_show_check = not self.child2_show_check
            if self.screen_paned.get_move_width() == 0:
                self.screen_paned.set_move_width(self.screen_paned.save_move_width)
                self.screen_paned.set_all_size()
            else:
                self.screen_paned.set_jmp_end()
                self.screen_paned.set_all_size()

    def close_right_child2(self):
        self.screen_paned.set_jmp_end() # 关闭右侧控件(播放列表..).

    def open_right_child2(self):
        self.screen_paned.set_jmp_start() # 打开右侧控件 (播放列表...).

    def hide_handle(self):
        self.screen_paned.set_visible_handle(False)

    def show_handle(self):
        self.screen_paned.set_visible_handle(True)


