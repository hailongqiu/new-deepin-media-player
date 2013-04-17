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



from widget.constant import SEEK_VALUE



class MediaPlayFun(object):
    def __init__(self, this):
        self.this = this
        self.__init_values()
        self.__init_ldmp_values()

    def __init_values(self):
        self.app = self.this.gui.app
        #
        self.__init_top_toolbar()
        self.__init_app_play_control_panel()
        self.__init_bottom_toolbar()
        #
        self.ldmp = self.this.ldmp
        self.list_view = self.this.gui.play_list_view.list_view
        self.list_view.connect_event("double-items",  self.list_view_double_items) 
        self.play_list = self.this.play_list

    def list_view_double_items(self, listview, double_items, row, col, item_x, item_y):
        self.play_list.set_items_index(double_items)
        self.this.play(double_items.sub_items[2].text)

    def __init_top_toolbar(self):
        self.keep_above_check = False
        self.top_toolbar    = self.this.gui.top_toolbar
        self.top_toolbar.toolbar_radio_button.set_full_state(False) # 初始化.
        self.top_toolbar.toolbar_above_button.connect("clicked", self.__top_toolbar_above_button_clicked)
        self.top_toolbar.toolbar_1X_button.connect("clicked",    self.__top_toolbar_1X_button_clicked)
        self.top_toolbar.toolbar_2X_button.connect("clicked",    self.__top_toolbar_2X_button_clicked)    
        self.top_toolbar.toolbar_concise_button.connect("clicked", self.__top_toolbar_concise_button_clicked)
        self.top_toolbar.toolbar_common_button.connect("clicked",  self.__top_toolbar_common_button_clicked) 
        self.top_toolbar.toolbar_full_button.connect("clicked", self.__top_toolbar_full_button_clicked) 

    def __init_app_play_control_panel(self):
        self.app_play_control_panel    = self.this.gui.play_control_panel
        self.app_play_control_panel.progressbar.connect("value-changed", self.__bottom_toolbar_pb_value_changed)
        self.app_play_control_panel.pb_fseek_btn.connect("clicked", self.__bottom_toolbar_pb_fseek_btn_clicked)
        self.app_play_control_panel.pb_bseek_btn.connect("clicked", self.__bottom_toolbar_pb_bseek_btn_clicked)
        self.app_play_control_panel.play_list_btn.button.connect("clicked", 
                 self.__app_play_control_panel_play_list_btn_clicked)
        start_button = self.app_play_control_panel.play_control_panel
        stop_button = self.app_play_control_panel.play_control_panel.stop_button
        pre_button  = self.app_play_control_panel.play_control_panel.pre_button
        next_button = self.app_play_control_panel.play_control_panel.next_button
        #
        start_button.start_button.connect("clicked", self.__bottom_toolbar_start_button_clicked)
        stop_button.connect("clicked",  self.__bottom_toolbar_stop_button_clicked)
        pre_button.connect("clicked", self.__pre_button_clicked)
        next_button.connect("clicked", self.__next_button_clicked)
        '''
            # 这里需要读 ini文件, 是否显示初始化的时候显示播放列表. 默认不显示播放列表.
            self.app_play_control_panel.play_list_btn.button.set_active(True)
        '''

    def __init_bottom_toolbar(self):
        self.bottom_play_control_panel = self.this.gui.bottom_toolbar.play_control_panel
        self.bottom_toolbar = self.this.gui.bottom_toolbar
        self.bottom_toolbar.progressbar.connect("value-changed", self.__bottom_toolbar_pb_value_changed)
        self.bottom_toolbar.pb_fseek_btn.connect("clicked",      self.__bottom_toolbar_pb_fseek_btn_clicked)
        self.bottom_toolbar.pb_bseek_btn.connect("clicked",      self.__bottom_toolbar_pb_bseek_btn_clicked)
        stop_button = self.bottom_toolbar.play_control_panel.stop_button
        start_button = self.bottom_toolbar.play_control_panel.start_button
        pre_button  = self.bottom_toolbar.play_control_panel.pre_button
        next_button = self.bottom_toolbar.play_control_panel.next_button
        stop_button.connect("clicked",  self.__bottom_toolbar_stop_button_clicked)
        start_button.connect("clicked", self.__bottom_toolbar_start_button_clicked)
        pre_button.connect("clicked", self.__pre_button_clicked)
        next_button.connect("clicked", self.__next_button_clicked)

    def __top_toolbar_1X_button_clicked(self, widget):
        print "__top_toolbar_1X_button_clicked..."

    def __top_toolbar_2X_button_clicked(self, widget):   
        print "__top_toolbar_2X_button_clicked..."

    def __top_toolbar_concise_button_clicked(self, widget):
        self.this.top_toolbar_concise_button_clicked()

    def __top_toolbar_common_button_clicked(self, widget):
        self.this.top_toolbar_common_button_clicked()

    def __top_toolbar_full_button_clicked(self, widget):
        self.this.fullscreen_function()

    def __top_toolbar_above_button_clicked(self, widget):
        if not self.keep_above_check:
            self.app.window.set_keep_above(True)
            self.keep_above_check = True
        else:
            self.app.window.set_keep_above(False)
            self.keep_above_check = False

    def __app_play_control_panel_play_list_btn_clicked(self, widget):
        # 设置右部的child2的 播放列表.
        child2_width = self.this.gui.screen_paned.get_move_width()
        self.this.gui.child2_show_check = not self.this.gui.child2_show_check
        if child2_width == 0:
            self.this.gui.open_right_child2()
            self.this.gui.screen_paned.set_all_size()
        else:
            self.this.gui.close_right_child2()
            self.this.gui.screen_paned.set_all_size()

    def __pre_button_clicked(self, widget):
        self.this.prev()

    def __next_button_clicked(self, widget):
        self.this.next()

    def __bottom_toolbar_pb_value_changed(self, pb, value):
        self.ldmp.seek(value)

    def __bottom_toolbar_pb_fseek_btn_clicked(self, widget):
        self.ldmp.fseek(SEEK_VALUE)

    def __bottom_toolbar_pb_bseek_btn_clicked(self, widget):
        self.ldmp.bseek(SEEK_VALUE)

    def __bottom_toolbar_stop_button_clicked(self, widget):
        print "__bottom_toolbar_stop_button_clicked...", widget
        print self.play_list.get_next_file()
        #print self.play_list.get_prev_file()

    def __bottom_toolbar_start_button_clicked(self, widget):
        print "__bottom_toolbar_start_button_clicked...", widget
        self.__start_button_clicked()
        
    def __stop_button_clicked(self):
        self.ldmp.stop()

    def __start_button_clicked(self):
        self.ldmp.pause()

    def __init_ldmp_values(self):
        self.__pos = "00:00:00 / "
        self.__length = "00:00:00"

    #######################################################
    ## @ldmp.
    def ldmp_start_media_player(self, ldmp):    
        self.bottom_toolbar.progressbar.set_sensitive(True)
        self.bottom_toolbar.pb_fseek_btn.set_sensitive(True)
        self.bottom_toolbar.pb_bseek_btn.set_sensitive(True)
        self.bottom_play_control_panel.start_button.set_start_bool(False)
        # 
        self.app_play_control_panel.progressbar.set_sensitive(True)
        self.app_play_control_panel.pb_fseek_btn.set_sensitive(True)
        self.app_play_control_panel.pb_bseek_btn.set_sensitive(True)
        self.app_play_control_panel.play_control_panel.start_button.set_start_bool(False)

    def ldmp_end_media_player(self, ldmp):
        # 改变所有的状态.
        self.__pos = "00:00:00 / "
        self.__length = "00:00:00"
        ''' 下部工具条 '''
        self.bottom_toolbar.show_time.set_time_font(self.__pos, self.__length)
        self.bottom_toolbar.progressbar.set_pos(0)
        self.bottom_toolbar.progressbar.set_sensitive(False)
        self.bottom_toolbar.pb_fseek_btn.set_sensitive(False)
        self.bottom_toolbar.pb_bseek_btn.set_sensitive(False)
        self.bottom_play_control_panel.start_button.set_start_bool(True)
        ''' 播放控制面板 '''
        self.app_play_control_panel.show_time.set_time_font(self.__pos, self.__length)
        self.app_play_control_panel.progressbar.set_pos(0)
        self.app_play_control_panel.progressbar.set_sensitive(False)
        self.app_play_control_panel.progressbar.set_sensitive(False)
        self.app_play_control_panel.pb_fseek_btn.set_sensitive(False)
        self.app_play_control_panel.pb_bseek_btn.set_sensitive(False)
        self.app_play_control_panel.play_control_panel.start_button.set_start_bool(True)

    def ldmp_pause_play(self, pause_check):
        if pause_check: # 正在播放.
            self.app_play_control_panel.play_control_panel.start_button.set_start_bool(False)
            self.bottom_play_control_panel.start_button.set_start_bool(False)
        else: # 暂停.
            self.app_play_control_panel.play_control_panel.start_button.set_start_bool(True)
            self.bottom_play_control_panel.start_button.set_start_bool(True)

    def ldmp_get_time_pos(self, ldmp, pos, time):
        # 设置显示的时间值.
        self.__set_pos_time(time)
        # 获取播放进度设置进度条.
        self.bottom_toolbar.progressbar.set_pos(pos)
        self.app_play_control_panel.progressbar.set_pos(pos)

    def ldmp_get_time_length(self, ldmp, length, time):    
        # 设置显示的总长度值.
        self.__set_length_time(time)
        # 获取播放总进度设置进度条的最大值.
        self.bottom_toolbar.progressbar.set_max_value(length)
        self.app_play_control_panel.progressbar.set_max_value(length)

    def __set_pos_time(self, time):
        self.__pos = str(time) + " / "
        self.bottom_toolbar.show_time.set_time_font(self.__pos, self.__length)
        self.app_play_control_panel.show_time.set_time_font(self.__pos, self.__length)

    def __set_length_time(self, time):
        self.__length = str(time)
        self.bottom_toolbar.show_time.set_time_font(self.__pos, self.__length)
        self.app_play_control_panel.show_time.set_time_font(self.__pos, self.__length)

