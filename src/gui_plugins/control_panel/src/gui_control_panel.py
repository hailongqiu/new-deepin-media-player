#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012 Deepin, Inc.
#               2012 Hailong Qiu
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

import dtk.ui.tooltip as Tooltip
from dtk.ui.label import Label
from dtk.ui.draw import draw_pixbuf
from dtk.ui.utils import propagate_expose
from dtk.ui.cache_pixbuf import CachePixbuf
from dtk.ui.button import ToggleButton
from skin import app_theme
from ini import Config
from utils import get_home_path, length_to_time, get_file_type
from utils import show_open_file_dialog_window
from mplayer.player import (STOPING_STATE, PAUSE_STATE, STARTING_STATE)
from locales import _
import gtk
import os

class BottomControlPanel(object):
    def __init__(self):
        # init values.
        self.load_check = True
        config_path = os.path.join(get_home_path(), ".config/deepin-media-player/deepin_media_config.ini")
        # 配置文件
        self.ini = Config(config_path)
        # 进度条.
        self.progressbar = gtk.Button("======progressbar==========")
        # 时间显示.
        self.show_time_label = ShowTime()
        self.show_time_label.set_time_text("00:00:00", "00:00:00")
        # 控制: 停止...下一曲,打开
        self.control_panel_ali = gtk.Alignment(0.5, 0, 0, 0)
        self.control_panel = ControlPanel()
        self.control_panel_ali.add(self.control_panel)
        # 打开播放列表.
        self.open_play_list_button = ToggleButton(
            app_theme.get_pixbuf("open_play_list_button/play_list_button.png"),
            app_theme.get_pixbuf("open_play_list_button/list_button_background.png"),
            )
        if self.ini.get("Window", "playlist") == "True":
            self.open_play_list_button.set_active(False)                
        #
        self.control_panel_hbox = gtk.HBox()
        self.control_panel_hbox.pack_start(self.show_time_label, False, False)
        self.control_panel_hbox.pack_start(self.control_panel_ali, True, True)
        self.control_panel_hbox.pack_start(gtk.Button("音量按钮"), False, False)
        self.control_panel_hbox.pack_start(self.open_play_list_button, False, False)                
        #
        self.control_panel.stop_button.connect("clicked", self.stop_button_clicked)
        self.control_panel.start_button.connect("clicked", self.start_button_clicked)
        self.control_panel.pre_button.connect("clicked", self.pre_button_clicked)
        self.control_panel.next_button.connect("clicked", self.next_button_clicked)
        self.control_panel.open_button.connect("clicked", self.open_button_clicked)        
        #
        self.open_play_list_button.connect("clicked", self.open_play_list_clicked)
        
    def stop_button_clicked(self, widget):
        self.ldmp.stop()
        
    def start_button_clicked(self, widget):
        if not self.this.play_list.get_sum(): # 判断播放列表是否为空.
            self.open_file_dialog_window_function()
        else:    
            if self.ldmp.player.state == STOPING_STATE:
                self.ldmp.play() # 播放文件.
            else:    
                self.ldmp.pause() # 暂停.
                if self.ldmp.player.state == STARTING_STATE:
                    Tooltip.text(self.control_panel.start_button, _("Pause"))
                else:    
                    Tooltip.text(self.control_panel.start_button, _("Start"))                    
                    
    def open_file_dialog_window_function(self):                
        # 打开文件对话框.
        play_file = show_open_file_dialog_window("深度影音开发对话框")
        if play_file:
            self.this.play_list.set_file(play_file)
            self.ldmp.quit()
            self.ldmp.player.uri = play_file
            gtk.timeout_add(88, lambda :self.ldmp.play())
        else:
            self.control_panel.start_button.set_start_bool(True)
        
    def pre_button_clicked(self, widget):    
        self.this.prev()

    def next_button_clicked(self, widget):    
        self.this.next()
        
    def open_button_clicked(self, widget):
        self.open_file_dialog_window_function()
        
    def open_play_list_clicked(self, widget):
        open_check = self.ini.get("Window", "playlist")
        if open_check == "True": # 隐藏播放列表
            self.ini.set("Window", "playlist", "False")                
            self.ini.save()
        else:    
            self.ini.set("Window", "playlist", "True")                
            self.ini.save()
                                        
    def init_values(self, this):
        self.this = this
        self.gui  = this.gui
        self.ldmp = this.ldmp
        self.ldmp.connect("get-time-pos", self.ldmp_get_time_pos)
        self.ldmp.connect("start-media-player", self.ldmp_start_media_player)
        self.ldmp.connect("end-media-player", self.ldmp_end_media_player)
        self.ldmp.connect("error-msg", self.ldmp_error_msg)
        
    def ldmp_get_time_pos(self, ldmp, pos, time):        
        self.show_time_label.set_time_text(
            length_to_time(self.ldmp.player.length),
            time
            )
                
    def ldmp_start_media_player(self, ldmp):    
        Tooltip.text(self.control_panel.start_button, _("Pause"))
        self.control_panel.start_button.set_start_bool(False) # 播放结束改变状态.
        
    def ldmp_end_media_player(self, ldmp):
        self.show_time_label.set_time_text("00:00:00", "00:00:00")
        self.control_panel.start_button.set_start_bool(True) # 播放结束改变状态.
        Tooltip.text(self.control_panel.start_button, _("Start"))
        
    def ldmp_error_msg(self, ldmp, error_code):
        pass
        
    def auto(self):
        return True
          
    def start(self):
        if self.load_check:
            self.gui.main_vbox.pack_start(self.progressbar, False, False)
            self.gui.main_vbox.pack_start(self.control_panel_hbox, False, False)
            self.gui.main_vbox.show_all()
            self.load_check = False
        
    def stop(self):    
        if not self.load_check:
            self.gui.main_vbox.remove(self.progressbar)
            self.gui.main_vbox.remove(self.control_panel_hbox)
            self.gui.main_vbox.show_all()
            self.load_check = True
   
def return_plugin(): 
    return BottomControlPanel

    
# 播放控制面板.
class ControlPanel(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self)
        # 停止按钮.
        self.stop_button = StartButton(
            app_theme.get_pixbuf("stop_button/stop_normal.png"),
            app_theme.get_pixbuf("stop_button/stop_hover.png"),
            app_theme.get_pixbuf("stop_button/stop_press.png"),
            app_theme.get_pixbuf("stop_button/stop_normal.png"),
            app_theme.get_pixbuf("stop_button/stop_hover.png"),
            app_theme.get_pixbuf("stop_button/stop_press.png")            
            )
        # 上一曲.
        self.pre_button = StartButton(
            app_theme.get_pixbuf("pre_button/pre_button_normal.png"),
            app_theme.get_pixbuf("pre_button/pre_button_hover.png"),
            app_theme.get_pixbuf("pre_button/pre_button_press.png"),
            app_theme.get_pixbuf("pre_button/pre_button_normal.png"),
            app_theme.get_pixbuf("pre_button/pre_button_hover.png"),
            app_theme.get_pixbuf("pre_button/pre_button_press.png")
            )
        # 开始/暂停.
        self.start_button = StartButton()
        # 下一曲.
        self.next_button = StartButton(
            app_theme.get_pixbuf("next_button/next_button_normal.png"),
            app_theme.get_pixbuf("next_button/next_button_hover.png"),
            app_theme.get_pixbuf("next_button/next_button_press.png"),
            app_theme.get_pixbuf("next_button/next_button_normal.png"),
            app_theme.get_pixbuf("next_button/next_button_hover.png"),
            app_theme.get_pixbuf("next_button/next_button_press.png")
            )
        # 打开按钮.
        self.open_button = StartButton(
            app_theme.get_pixbuf("open_button/open_normal.png"),
            app_theme.get_pixbuf("open_button/open_hover.png"),
            app_theme.get_pixbuf("open_button/open_press.png"),
            app_theme.get_pixbuf("open_button/open_normal.png"),
            app_theme.get_pixbuf("open_button/open_hover.png"),
            app_theme.get_pixbuf("open_button/open_press.png")
            )
        # 设置提示信息.
        Tooltip.text(self.stop_button, _("Stop"))
        Tooltip.text(self.pre_button, _("Pre"))
        Tooltip.text(self.start_button, _("Play"))        
        Tooltip.text(self.next_button, _("Next"))        
        Tooltip.text(self.open_button, _("Open"))
        
        self.pack_start(self.stop_button, False, False)
        self.pack_start(self.pre_button, False, False)
        self.pack_start(self.start_button, False, False)
        self.pack_start(self.next_button, False, False)
        self.pack_start(self.open_button, False, False)

        
        
class StartButton(gtk.Button):
    def __init__(self,                 
                 start_button_normal=app_theme.get_pixbuf("start_button/play_button_normal.png"),
                 start_button_hover=app_theme.get_pixbuf("start_button/play_button_hover.png"),
                 start_button_press=app_theme.get_pixbuf("start_button/play_button_press.png"),
                 pause_button_normal=app_theme.get_pixbuf("start_button/pause_button_normal.png"),
                 pause_button_hover=app_theme.get_pixbuf("start_button/pause_button_hover.png"),
                 pause_button_press=app_theme.get_pixbuf("start_button/pause_button_press.png"),
                 image_y_padding=-2):
        
        gtk.Button.__init__(self)
        self.image_y_padding = image_y_padding
        self.start_bool = True
        self.stop_bool = False
        self.start_button_normal = start_button_normal
        self.start_button_hover = start_button_hover
        self.start_button_press = start_button_press
        
        self.pause_button_normal = pause_button_normal
        self.pause_button_hover = pause_button_hover
        self.pause_button_press = pause_button_press
        
        self.connect("expose-event", self.expose_button)
        self.connect("clicked", self.clicked_button)
        
        self.cache_pixbuf = CachePixbuf()
        
    def clicked_button(self, widget):
        self.set_start_bool(not self.start_bool)
                
    def set_start_bool(self, start_bool):    
        if not self.stop_bool:
            self.start_bool = start_bool            
            self.queue_draw()
            
    def set_stop_bool(self, stop_bool):
        self.stop_bool = stop_bool
            
    def expose_button(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        x,y,w,h = rect.x, rect.y, rect.width, rect.height
                    
        if widget.state == gtk.STATE_NORMAL:
            if self.start_bool:                
                image = self.start_button_normal.get_pixbuf()
            else:
                image = self.pause_button_normal.get_pixbuf()                
        elif widget.state == gtk.STATE_PRELIGHT:
            if self.start_bool:
                image = self.start_button_hover.get_pixbuf()
            else:    
                image = self.pause_button_hover.get_pixbuf()
        elif widget.state == gtk.STATE_ACTIVE:
            if self.start_bool:
                image = self.start_button_press.get_pixbuf()
            else:    
                image = self.pause_button_press.get_pixbuf()

        widget.set_size_request(image.get_width(), image.get_height())
        self.cache_pixbuf.scale(image, image.get_width(), image.get_height())        
        draw_pixbuf(cr, self.cache_pixbuf.get_cache(), widget.allocation.x, widget.allocation.y - self.image_y_padding)
        
        # Set widget size.
        propagate_expose(widget, event)
        return True
        
# 显示播放时间.
class ShowTime(Label):
    '''显示播放时间'''
    def __init__(self):     
        Label.__init__(self, "", enable_gaussian=True)
        self.time_text_1 = ""
        self.time_text_2 = ""
        
    def set_time_text(self, time_text_1, time_text_2):    
        self.time_text_1 = str(time_text_1)
        self.time_text_2 = str(time_text_2)        
        self.set_text(self.time_text_1 + " / " + self.time_text_2)
