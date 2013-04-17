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
from user_guide import init_user_guide
from widget.constant import SEEK_VALUE
from widget.constant import VOLUME_VALUE
from mplayer.player import ASCEPT_4X3_STATE, ASCEPT_16X9_STATE, ASCEPT_5X4_STATE
from mplayer.player import ASCEPT_16X10_STATE, ASCEPT_1_85X1_STATE, ASCEPT_2_35X1_STATE
from mplayer.player import ASCEPT_FULL_STATE, ASCEPT_DEFULAT
from mplayer.playlist import SINGLA_PLAY, ORDER_PLAY, RANDOM_PLAY, SINGLE_LOOP, LIST_LOOP 

class MediaPlayMenus(object):
    def __init__(self, this):
        self.this = this
        self.gui  = self.this.gui
        self.ldmp = self.this.ldmp
        self.ldmp.connect("volume-play", self.test_ldmp_mute_play)
        self.play_list = self.this.play_list
        self.list_view = self.this.gui.play_list_view.list_view
        # test 播放列表弹出.
        self.list_view.connect_event("right-items-event", self.list_veiw_test_show_menu)
        self.menus = self.this.gui.play_menus
        # 初始化连接事件.
        self.menus.full_screen  = self.this.fullscreen_function
        self.menus.normal_mode  = self.this.top_toolbar_common_button_clicked
        self.menus.compact_mode = self.this.top_toolbar_concise_button_clicked
        #
        self.menus.next         = self.this.next
        self.menus.prev         = self.this.prev
        self.menus.fseek        = self.menu_fseek
        self.menus.bseek        = self.menu_bseek
        #
        self.menus.stereo_channel = self.menu_stereo_channel  # 立体声.
        self.menus.left_channel   = self.menu_left_channel 
        self.menus.right_channel  = self.menu_right_channel 
        self.menus.mute_unmute    = self.menu_mute_unmute
        self.menus.inc_volume     = self.menu_inc_volume
        self.menus.dec_volume     = self.menu_dec_volume
        # 初始化 声道 为立体声.
        self.menu_stereo_channel()
        #
        self.menus.config_gui = self.this.config_gui
        self.menus.quit       = self.menu_quit
        self.menus.init_user_guide = init_user_guide
        # 设置播放比例.
        self.menus.normal_ascept   = self.menu_normal_ascept
        self.menus._4X3_ascept     = self.menu_4X3_ascept
        self.menus._16X9_ascept    = self.menu_16X9_ascept
        self.menus._16X10_ascept   = self.menu_16X10_ascept
        self.menus._1_85X1_ascept  = self.menu_1_85X1_ascept
        self.menus._2_35X1_ascept  = self.menu_2_35X1_ascept
        # 初始化为默认.
        self.set_menu_ascept(0, ASCEPT_DEFULAT)
        # 设置播放状态.
        # 播放列表 .       0        1       2         3          4
        #           { 单曲播放、顺序播放、随机播放、单曲循环播放、列表循环播放、}
        #            SINGLA_PLAY ... ...                ...LIST_LOOP
        self.menus.play_track            = self.menu_play_track
        self.menus.play_default          = self.menu_play_default
        self.menus.play_random           = self.menu_play_random
        self.menus.play_repeat_track     = self.menu_play_repeat_track
        self.menus.play_repeat_play_list = self.menu_play_repeat_play_list
        # 初始化为顺序播放.
        self.set_play_list_state(1, ORDER_PLAY)
        ############################
        # 修改图标.
        #self.menus.title_root_menu.menu_items[0].set_item_icons((pixbuf, pixbuf, pixbuf))
        # 禁止图标.
        #self.menus.title_root_menu.set_menu_item_sensitive_by_index(1, False)
        #self.menus.play_state_menu.menu_items[1].set_item_icons((pixbuf, pixbuf1, pixbuf2))
        #self.menus.play_state_menu.set_mutual_icons(2, (pixbuf, pixbuf1, pixbuf2))
        #self.menus.video_menu.set_mutual_icons(0, (pixbuf, pixbuf1, pixbuf2))

    def test_ldmp_mute_play(self, ldmp, mute_check):
        print "volume:", mute_check

    def list_veiw_test_show_menu(self, list_view, event, row_index, col_index, item_x, item_y):
        self.menus.show_play_list_menu(event)

    def menu_quit(self):
        self.ldmp.quit()
        self.gui.app.window.destroy()

    def menu_fseek(self):
        self.ldmp.fseek(SEEK_VALUE)

    def menu_bseek(self):
        self.ldmp.bseek(SEEK_VALUE)

    def menu_stereo_channel(self):
        self.ldmp.normalchannel()
        self.set_audio_menu_state(0)

    def menu_left_channel(self):
        self.ldmp.leftchannel()
        self.set_audio_menu_state(1)

    def menu_right_channel(self):
        self.ldmp.rightchannel()
        self.set_audio_menu_state(2)

    def set_audio_menu_state(self, index):
        self.menus.channel_select_menu.set_mutual_icons(index,
                  (self.menus.video_aspect_pixbuf, 
                   self.menus.video_aspect_select_pixbuf, 
                   self.menus.video_aspect_none_pixbuf))

    def menu_mute_unmute(self):
        self.this.mute_umute()

    def menu_inc_volume(self):
        #self.ldmp.addvolume(VOLUME_VALUE)
        #self.ldmp.setvolume(90)
        pass
        print "menu_inc_volume.."

    def menu_dec_volume(self):
        #self.ldmp.decvolume(VOLUME_VALUE)
        print "menu_dec_volume..."

    def menu_normal_ascept(self):
        # 默认.
        self.set_menu_ascept(0, ASCEPT_DEFULAT)

    def menu_4X3_ascept(self):
        # 4:3.
        self.set_menu_ascept(1, ASCEPT_4X3_STATE)

    def menu_16X9_ascept(self):
        # 16:9.
        self.set_menu_ascept(2, ASCEPT_16X9_STATE)

    def menu_16X10_ascept(self):
        # 16:10.
        self.set_menu_ascept(3, ASCEPT_16X10_STATE)

    def menu_1_85X1_ascept(self):
        # 1.85:1 比例.
        self.set_menu_ascept(4, ASCEPT_1_85X1_STATE)

    def menu_2_35X1_ascept(self):
        # 2.35:1 比例.
        self.set_menu_ascept(5, ASCEPT_2_35X1_STATE)

    def set_menu_ascept(self, index, state):
        self.menus.video_menu.set_mutual_icons(index, 
                  (self.menus.video_aspect_pixbuf, 
                   self.menus.video_aspect_select_pixbuf, 
                   self.menus.video_aspect_none_pixbuf))
        self.ldmp.player.ascept_state = state
        self.this.set_ascept_restart()

    #SINGLA_PLAY, ORDER_PLAY, RANDOM_PLAY, SINGLE_LOOP, LIST_LOOP 
    def menu_play_track(self):
        self.set_play_list_state(0, SINGLA_PLAY)

    def menu_play_default(self):
        self.set_play_list_state(1, ORDER_PLAY)

    def menu_play_random(self):
        self.set_play_list_state(2, RANDOM_PLAY)

    def menu_play_repeat_track(self):
        self.set_play_list_state(3, SINGLE_LOOP)

    def menu_play_repeat_play_list(self):
        self.set_play_list_state(4, LIST_LOOP)

    def set_play_list_state(self, index, state):
        self.play_list.set_state(state)
        self.menus.play_state_menu.set_mutual_icons(index,
                  (self.menus.video_aspect_pixbuf, 
                   self.menus.video_aspect_select_pixbuf, 
                   self.menus.video_aspect_none_pixbuf))






