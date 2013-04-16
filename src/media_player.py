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



from skin import app_theme
import dtk.ui.tooltip as Tooltip
from dtk.ui.draw import draw_pixbuf
from dtk.ui.utils import color_hex_to_cairo
from locales import _ # 国际化翻译.
from widget.utils import get_home_path
from widget.keymap import get_keyevent_name
from plugin_manage import PluginManage
from gui import GUI # 播放器界面布局.
from media_player_function import MediaPlayFun
from mplayer.timer import Timer
# mplayer后端.
from mplayer.player import LDMP, set_ascept_function, unset_flags, set_flags
from mplayer.player import STARTING_STATE, PAUSE_STATE
from mplayer.player import ASCEPT_4X3_STATE, ASCEPT_16X9_STATE, ASCEPT_5X4_STATE
from mplayer.player import ASCEPT_16X10_STATE, ASCEPT_1_85X1_STATE, ASCEPT_2_35X1_STATE, ASCEPT_FULL_STATE, ASCEPT_DEFULAT
from mplayer.player import (ERROR_RETRY_WITH_MMSHTTP, ERROR_RESOLVE_AF_INET, ERROR_SOCKET_CONNECT,
                            ERROR_FILE_FORMAT, ERROR_DVD_DEVICE, ERROR_RETRY_ALSA_BUSY,
                            ERROR_RETRY_WITH_HTTP, ERROR_RETRY_WITH_HTTP_AND_PLAYLIST,
                            ERROR_RETRY_WITH_PLAYLIST)
from mplayer.player import TYPE_FILE, TYPE_CD, TYPE_DVD, TYPE_VCD, TYPE_NETWORK, TYPE_DVB, TYPE_TV
from mplayer.playlist import PlayList, SINGLA_PLAY, ORDER_PLAY, RANDOM_PLAY, SINGLE_LOOP, LIST_LOOP 
# 播放列表 .       0        1       2         3          4
#           { 单曲播放、顺序播放、随机播放、单曲循环播放、列表循环播放、}
#            SINGLA_PLAY ... ...                ...LIST_LOOP
import random
import time
import gtk
import sys
import os

class MediaPlayer(object):
    def __init__(self):
        self.__init_dbus_id()
        self.__init_values()
        # init double timer.
        self.__init_double_timer()
        self.__init_move_window()
        self.__init_gui_app_events()
        self.__init_gui_screen()
        # show gui window.
        self.gui.app.window.show_all()
        self.gui.screen.window.set_composited(True)
        # 全部的执行函数方法.
        self.media_play_fun = MediaPlayFun(self)

    def __init_dbus_id(self): # 初始化DBUS ID 唯一值.
        dbus_id_list = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())).split("-")
        dbus_id = ""
        dbus_id_list[0] = random.randint(0, 1000)
        dbus_id_list[1] = random.randint(0, 1000)
        dbus_id_list[2] = random.randint(0, 1000)
        dbus_id_list[3] = random.randint(0, 1000)
        for num in dbus_id_list:
            number = int(num) + 65
            if ((65 <= number and number <= 90 ) or (97 <= number and number <= 122)):
                dbus_id += "." + chr(number)
            else:
                dbus_id += "." + chr(random.randint(65, 90))
        print "dbus_id:", dbus_id
        self.dbus_id = dbus_id

    def __init_values(self):
        self.keymap = {} # 快捷键.
        self.keymap["Escape"]  = self.key_quit_fullscreen
        self.keymap["Return"]  = self.fullscreen_function
        self.keymap["Space"]   = self.key_pause
        self.keymap["Shift + Return"] = self.key_concise_mode
        #
        self.ldmp = LDMP()
        self.gui = GUI()        
        self.play_list = PlayList(self.gui.play_list_view.list_view) 
        # 初始化播放列表.
        self.play_list.set_file_list(self.gui.play_list_view.list_view.items)
        #self.plugin_manage = PluginManage()
        self.fullscreen_check = False # 全屏
        self.concise_check    = False # 简洁模式 # True 简洁模式 False 普通模式
        #
        #SINGLA_PLAY, ORDER_PLAY, RANDOM_PLAY, SINGLE_LOOP, LIST_LOOP 
        self.play_list.set_state(RANDOM_PLAY)
        self.argv_path_list = sys.argv # save command argv.        

    def __init_double_timer(self):
        self.interval = 300
        self.timer = Timer(self.interval)
        self.double_check = False
        self.save_double_x = 0
        self.save_double_y = 0
        self.timer.connect("Tick", self.timer_tick_event)

    def __init_move_window(self):
        self.move_win_check = False
        self.save_move_button = None
        self.save_move_time   = None
        self.save_move_x = 0
        self.save_move_y = 0

    def __init_gui_app_events(self):
        '''application events init.'''
        self.gui.app.titlebar.min_button.connect("clicked", self.app_window_min_button_clicked)        
        self.gui.app.window.connect("destroy", self.app_window_quit)
        self.gui.app.window.connect("configure-event", self.app_window_configure_event)
        self.gui.app.window.connect("check-resize", self.app_window_check_resize)
        # self.app.window.connect("window-state-event", )
        # self.app.window.connect("leave-notify-event", )
        # self.app.window.connect("focus-out-event", )
        # self.app.window.connect("focus-in-event", )
        self.gui.app.window.connect("key-press-event", self.app_window_key_press_event)
        # self.app.window.connect("key-release-event", )
        # self.app.window.connect("scroll_event", )
        # self.app.window.connect("check-resize",)         

    def app_window_key_press_event(self, widget, event):
        keyval_name = get_keyevent_name(event)
        print "name:", keyval_name
        if self.keymap.has_key(keyval_name):
            self.keymap[keyval_name]()

    def __init_gui_screen(self):
        '''screen events init.'''
        self.draw_check = True
        self.background = app_theme.get_pixbuf("player.png").get_pixbuf()        
        self.gui.screen_frame_event.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.gui.screen.connect("realize",            self.init_media_player)
        self.gui.screen.connect("expose-event",       self.screen_expose_event)
        self.gui.screen.connect("configure-event",    self.screen_configure_event)
        self.gui.screen_frame.connect("expose-event", self.screen_frame_expose_event)
        self.gui.screen_frame_event.connect("button-press-event",   self.screen_frame_event_button_press_event)
        self.gui.screen_frame_event.connect("button-release-event", self.screen_frame_event_button_release_event)
        self.gui.screen_frame_event.connect("motion-notify-event",  self.screen_frame_event_button_motoin_notify_event)
        self.gui.screen_frame_event.connect("leave-notify-event", self.screen_frame_event_leave_notify_event)

    def init_plugin_manage(self): # 初始化插件系统.
        # 加载自带插件.
        for zip_file in os.listdir("plugins"):
            try:
                self.plugin_manage.load_zip(os.path.join("plugins", zip_file))
            except Exception, e:        
                print "init_plugin_manage[error]:", e
                
        # 加载用户编写的插件.
        self.plugin_manage.load_dir()
        
        for plugin in self.plugin_manage.plugins_list:
            # if not plugin.name() in zip_name_list:
            if plugin.auto():
                plugin.init_values(self, self.gui, self.ldmp)
                plugin.start()
        
    '''application event conect function.窗口事件连接函数.'''
    def app_window_min_button_clicked(self, widget): # 缩小按钮单击.
        print "app_window_min_button_clicked function", "-->>min window!!"
        
    def app_window_quit(self, widget): # 窗口销毁.destroy
        self.ldmp.quit()
        
    def app_window_configure_event(self, widget, event): # configure-event
        self.set_ascept_restart() # 设置分辨率.
        
    def app_window_check_resize(self, widget):# check-resize    
        self.set_ascept_restart() # 设置分辨率.
        
    def set_ascept_restart(self):    
        try:            
            unset_flags(self.gui.screen)
            if self.ldmp.player.video_width == 0 or self.ldmp.player.video_height == 0:
                set_flags(self.gui.screen)
                ascept_num = None
            elif self.ldmp.player.ascept_state == ASCEPT_4X3_STATE:
                ascept_num = 4.0/3.0
            elif self.ldmp.player.ascept_state == ASCEPT_16X9_STATE:    
                ascept_num = 16.0/9.0
            elif self.ldmp.player.ascept_state == ASCEPT_16X10_STATE:    
                ascept_num = 16.0/10.0
            elif self.ldmp.player.ascept_state == ASCEPT_1_85X1_STATE:    
                ascept_num = 1.85/1.0
            elif self.ldmp.player.ascept_state == ASCEPT_5X4_STATE:    
                ascept_num = 5.0/4.0
            elif self.ldmp.player.ascept_state == ASCEPT_2_35X1_STATE:    
                ascept_num = 2.35/1.0
            elif self.ldmp.player.ascept_state == ASCEPT_FULL_STATE:
                ascept_num = None
            elif self.ldmp.player.ascept_state == ASCEPT_DEFULAT:
                ascept_num = float(self.ldmp.player.video_width) / float(self.ldmp.player.video_height)
            else:
                ascept_num = None
                set_flags(self.gui.screen)
            # set ascept.    
            set_ascept_function(self.gui.screen_frame, ascept_num)
        except Exception, e:
            set_ascept_function(self.gui.screen_frame, None)
            print "set_ascept_restart[error]:", e
            
    '''screen event conect function.播放屏幕事件连接函数'''
    def screen_frame_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(rect.x, rect.y, rect.width, rect.height)
        cr.fill()
        
    def init_media_player(self, widget): # screen realize.        
        '''初始化mplayer后端'''
        self.ldmp.xid = widget.window.xid
        self.ldmp.connect("get-time-pos",       self.ldmp_get_time_pos)
        self.ldmp.connect("get-time-length",    self.ldmp_get_time_length)
        self.ldmp.connect("end-media-player",   self.ldmp_end_media_player)
        self.ldmp.connect("start-media-player", self.ldmp_start_media_player)
        self.ldmp.connect("screen-changed",     self.ldmp_screen_changed)
        self.ldmp.connect("pause-play",         self.ldmp_pause_play)
        self.ldmp.connect("error-msg",          self.ldmp_error_msg)
        
        # self.ldmp.player.ascept_state = ASCEPT_16X10_STATE
        # self.ldmp.player.vo = "vdpau"
        # self.ldmp.player.type = TYPE_NETWORK
        # self.ldmp.player.ascept_state = ASCEPT_4X3_STATE
        # self.ldmp.player.flip_screen = "mirror"
        # self.ldmp.player.flip_screen = "rotate=2"
        # self.ldmp.player.uri = "mms://mediasrv2.iptv.xmg.com.cn/tvyingshi"        
        #self.ldmp.player.uri = "mms://112.230.192.196/zb10"
        self.ldmp.player.uri = "/home/long/视频/test4.mkv"
        #self.ldmp.player.cache_size = 1000
        self.ldmp.play()                
        # 初始化插件系统.
        #self.init_plugin_manage()
        
    def ldmp_get_time_pos(self, ldmp, pos, time):
        # print "pos:", pos
        self.media_play_fun.ldmp_get_time_pos(ldmp, pos, time)
        
        
    def ldmp_get_time_length(self, ldmp, length, time):    
        # print "length:", length, time
        self.media_play_fun.ldmp_get_time_length(ldmp, length, time)
        
    def ldmp_start_media_player(self, ldmp):    
        print "开始播放了..."
        self.player_start_init()
        self.media_play_fun.ldmp_start_media_player(ldmp)
        
    def player_start_init(self):    
        pass
    
    def ldmp_end_media_player(self, ldmp):
        print "播放结束!!", ldmp.player.type
        self.player_end_init()
        self.media_play_fun.ldmp_end_media_player(ldmp)
        
    def player_end_init(self):        
        # 播放完毕，重置播放设置.
        self.ldmp.player.video_width = 0
        self.ldmp.player.video_height = 0
        self.set_draw_background(0, 0)
        
    def ldmp_screen_changed(self, ldmp, video_width, video_height):
        #print "ldmp_screen_changed...", "video_width:", video_width, "video_height:", video_height
        self.set_draw_background(video_width, video_height) # 是否画播放器屏幕显示的背景.
        
    def set_draw_background(self, video_width, video_height):
        if video_width == 0 or video_height == 0:            
            self.draw_check = True # 是否画logo.
        else:
            self.draw_check = False
        self.set_ascept_restart() # 改变屏幕比例.    
        
    def ldmp_pause_play(self, ldmp, pause_check): # 暂停状态.
        self.media_play_fun.ldmp_pause_play(pause_check)

    def ldmp_error_msg(self, ldmp, error_code): # 接收后端错误信息.
        print "ldmp_error_msg->error_code:", error_code
        
    def screen_expose_event(self, widget, event):    
        cr = widget.window.cairo_create()
        rect = widget.allocation
        if self.draw_check: # 是否画播放器屏幕显示的背景.
            # 画周围logo黑边.
            cr.set_source_rgb(*color_hex_to_cairo("#0D0D0D")) # 1f1f1f
            cr.rectangle(rect.x, rect.y, rect.width, rect.height)
            cr.fill()
            # draw deepin media player logo.
            draw_pixbuf(cr,
                        self.background, 
                        rect.x + rect.width/2 - self.background.get_width()/2, 
                        rect.y + rect.height/2 - self.background.get_height()/2)

    def screen_configure_event(self, widget, event):
        self.set_ascept_restart() # 设置分辨率.

    def screen_frame_event_button_press_event(self, widget, event):
        if event.button == 1:
            self.save_double_data(event)
            self.save_move_data(event)

    def save_double_data(self, event):
        # 保存双击 x_root 和 y_root 坐标, 用于判断是否单击/双击区域内.
        self.save_double_x = int(event.x_root)
        self.save_double_y = int(event.y_root)

    def save_move_data(self, event):
        # 保存 event 的 button, x_root, y_root, time, 用于移动窗口.
        self.save_move_button = event.button
        self.save_move_x = int(event.x_root)
        self.save_move_y = int(event.y_root)
        self.save_move_time = event.time
        # 设置移动标志位.
        self.move_win_check = True

    def screen_frame_event_button_release_event(self, widget, event): # 连接屏幕单击/双击事件.
        if event.button == 1:
            # setting screen paned handle.
            self.gui.set_paned_handle(event)
            # move app window.
            self.run_double_and_click(event)

    def run_double_and_click(self, event):
        self.move_win_check = False # 取消移动窗口.
        new_double_x = int(event.x_root)
        new_double_y = int(event.y_root)
        double_width = 5
        # 判断如果点击下去移动了以后的距离,才进行单击和双击.
        if self.gui.not_in_system_widget():
            if ((self.save_double_x - double_width <= new_double_x <= self.save_double_x + double_width) and 
                (self.save_double_y - double_width <= new_double_y <= self.save_double_y + double_width)):
                if not self.timer.Enabled:
                    self.timer.Interval = self.interval
                    self.timer.Enabled = True
                else:
                    self.double_check  = True

                if self.timer.Enabled and self.double_check:
                    self.double_clicked_connect_function() # 执行双击的代码.
                    self.set_double_bit_false()
            else:
                self.set_double_bit_false()
            
    def timer_tick_event(self, tick):
        self.click_connect_function() # 执行单击的代码.
        self.set_double_bit_false()

    def double_clicked_connect_function(self):
        #print "你双击了............."
        self.fullscreen_function() # 全屏和退出全屏处理函数.

    def fullscreen_function(self):
        if not self.fullscreen_check: # 判断是否全屏.
            self.concise_mode() # 简洁模式.
            self.gui.app.window.fullscreen() # 全屏.
            self.fullscreen_check = True
        else:
            self.gui.app.window.unfullscreen()
            if not self.concise_check: # 如果是简洁模式,不普通模式.
                self.normal_mode() # 普通模式.
            self.fullscreen_check = False

    def concise_mode(self): # 简洁模式调用.
        # 左边部件child2操作.
        self.gui.close_right_child2()
        self.gui.screen_paned.set_all_size()
        self.gui.hide_handle()
        #
        self.gui.hide_play_control_paned()
        self.gui.main_ali.set_padding(0, 0, 0, 0) # 设置下,左右的距离.
        self.gui.app.hide_titlebar() # 隐藏标题栏.

    def normal_mode(self): # 普通模式调用.
        self.gui.main_ali.set_padding(0, 2, 2, 2)
        self.gui.app.show_titlebar()
        # 左边部件child2操作.
        self.gui.show_handle()
        self.gui.show_play_control_paned()
        if self.gui.child2_show_check:
            self.gui.open_right_child2() 
            self.gui.screen_paned.set_all_size()

    def click_connect_function(self):
        # 暂停/继续. 
        # 应该去连接后端事件,暂停/播放的时候去改变按钮状态.
        self.ldmp.pause()

    def set_double_bit_false(self):
        self.double_check = False
        self.timer.Enabled = False

    def screen_frame_event_button_motoin_notify_event(self, widget, event):
        if self.move_win_check:
            self.move_window_function(event)
        # 显示下部工具条.
        if (self.__in_bottom_window_check(widget, event) and 
            (self.fullscreen_check or self.concise_check)):
            self.gui.screen_paned.bottom_window.show()
            self.gui.screen_paned.bottom_win_show_check = True

    def move_window_function(self, event): # move window 移动窗口.
        if self.gui.not_in_system_widget():
            move_width = 5
            new_move_x = int(event.x_root)
            new_move_y = int(event.y_root)
            if not ((self.save_move_x - move_width <= new_move_x <= self.save_move_x + move_width) and 
                (self.save_move_y - move_width <= new_move_y <= self.save_move_y + move_width)):
                self.gui.app.window.begin_move_drag(self.save_move_button, 
                                                    self.save_move_x, 
                                                    self.save_move_y, 
                                                    self.save_move_time) 

    def screen_frame_event_leave_notify_event(self, widget, event):
        # 隐藏下部工具条.
        if event.window == self.gui.screen_frame.window:
            self.gui.screen_paned.bottom_window.hide()
            self.gui.screen_paned.bottom_win_show_check = False
            if (self.__in_bottom_window_check(widget, event) and 
                (self.fullscreen_check or self.concise_check)):
                self.gui.screen_paned.bottom_window.show()
                self.gui.screen_paned.bottom_win_show_check = True

    def __in_bottom_window_check(self, widget, event):
        if event.window == self.gui.screen_paned.window:
            min_x = 0
            max_x = self.gui.screen_paned.top_window.get_size()[0]
            min_y = widget.allocation.height - self.gui.screen_paned.bottom_win_h
            max_y = widget.allocation.height
            return ((min_y <= int(event.y) < max_y) and 
                (min_x <= int(event.x) < max_x))
    # 上一曲.
    def prev(self):    
        play_file = self.play_list.get_prev_file()
        if play_file:
            self.ldmp.quit()
            gtk.timeout_add(88, self.timeout_prev, play_file)
            
    def timeout_prev(self, play_file):
        self.ldmp.player.uri = play_file
        self.ldmp.play()
    
    # 下一曲.
    def next(self):    
        play_file = self.play_list.get_next_file()
        if play_file:
            self.ldmp.quit()
            gtk.timeout_add(88, self.timeout_next, play_file)
        
    def timeout_next(self, play_file):        
        self.ldmp.player.uri = play_file
        self.ldmp.play()                
        
    def open_file_dialog(self):
        # 多选文件对话框.
        open_dialog = gtk.FileChooserDialog(_("Select Files"),
                                            None,
                                            gtk.FILE_CHOOSER_ACTION_OPEN,
                                            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                             gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        open_dialog.set_current_folder(get_home_path())
        open_dialog.set_select_multiple(True) # 多选文件.
        res = open_dialog.run()
        if res == gtk.RESPONSE_OK:
            print open_dialog.get_filenames()
        open_dialog.destroy()

    def open_dir_dialog(self):
        # 多选目录对话框.
        open_dialog = gtk.FileChooserDialog(_("Select Directory"),
                                            None,
                                            gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                             gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        open_dialog.set_current_folder(get_home_path())
        open_dialog.set_select_multiple(True) # 多选文件.
        res = open_dialog.run()
        if res == gtk.RESPONSE_OK:
            print open_dialog.get_filenames()
        open_dialog.destroy()

    ######################################################
    ## keymap press event
    def key_concise_mode(self):
        if self.fullscreen_check:
            self.fullscreen_function()
        if not self.concise_check:
            if self.fullscreen_check:
                self.fullscreen_function()
            self.concise_mode()
            self.concise_check = True
        else:
            self.normal_mode()
            self.concise_check = False

    def key_quit_fullscreen(self):
        if self.fullscreen_check:
            self.fullscreen_function()

    def key_pause(self):
        self.ldmp.pause()
