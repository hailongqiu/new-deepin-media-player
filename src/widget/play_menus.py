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


from dtk.ui.menu import Menu
from dtk.ui.utils import get_widget_root_coordinate
from dtk.ui.constant import WIDGET_POS_BOTTOM_LEFT
from skin import app_theme
from locales import _

class PlayMenus(object):
    def __init__(self):
        pass
        #self.init_system_pixbuf()
        self.__init_menus()
        
    def init_system_pixbuf(self):    
        # menu icon pixbuf. menupixbuf ..
        self.video_aspect_pixbuf = app_theme.get_pixbuf("screen/check_normal.png") # aspect state pixbuf.
        self.video_aspect_select_pixbuf = app_theme.get_pixbuf("screen/check_hover.png")
        self.video_aspect_none_pixbuf = app_theme.get_pixbuf("screen/check_none.png")
        self.video_aspect_type = ASCEPT_NORMAL_STATE #"默认"
        self.playwinmax_bool = True
        # concie pixbuf.
        self.menu_concie_normal_pixbuf = app_theme.get_pixbuf("screen/menu_concise_normal.png")
        self.menu_concie_hover_pixbuf = app_theme.get_pixbuf("screen/menu_concise_hover.png")
        self.menu_concie_none_pixbuf = app_theme.get_pixbuf("screen/menu_concise_none.png")
        # window mode.
        self.menu_window_mode_normal_pixbuf = app_theme.get_pixbuf("screen/menu_window_mode_normal.png")
        self.menu_window_mode_hover_pixbuf = app_theme.get_pixbuf("screen/menu_window_mode_hover.png")
        self.menu_window_mode_none_pixbuf = app_theme.get_pixbuf("screen/menu_window_mode_none.png")
        # play sequence.
        self.menu_play_sequence_normal_pixbuf = app_theme.get_pixbuf("screen/menu_play_sequence_normal.png")
        self.menu_play_sequence_hover_pixbuf = app_theme.get_pixbuf("screen/menu_play_sequence_hover.png")
        self.menu_play_sequence_none_pixbuf = app_theme.get_pixbuf("screen/menu_play_sequence_none.png")
        # full .
        self.menu_full_normal_pixbuf = app_theme.get_pixbuf("screen/menu_full_normal.png") 
        self.menu_full_hover_pixbuf = app_theme.get_pixbuf("screen/menu_full_hover.png")
        self.menu_full_none_pixbuf = app_theme.get_pixbuf("screen/menu_full_none.png")
        # pre.
        self.menu_pre_normal_pixbuf = app_theme.get_pixbuf("screen/menu_pre_normal.png")
        self.menu_pre_hover_pixbuf = app_theme.get_pixbuf("screen/menu_pre_hover.png")
        self.menu_pre_none_pixbuf = app_theme.get_pixbuf("screen/menu_pre_none.png")
        # next.
        self.menu_next_normal_pixbuf = app_theme.get_pixbuf("screen/menu_next_normal.png")
        self.menu_next_hover_pixbuf = app_theme.get_pixbuf("screen/menu_next_hover.png")        
        self.menu_next_none_pixbuf = app_theme.get_pixbuf("screen/menu_next_none.png")        
        # f seek 5.
        self.menu_f_seek_5_normal_pixbuf = app_theme.get_pixbuf("screen/menu_f_seek_5_normal.png")
        self.menu_f_seek_5_hover_pixbuf = app_theme.get_pixbuf("screen/menu_f_seek_5_hover.png")
        self.menu_f_seek_5_none_pixbuf = app_theme.get_pixbuf("screen/menu_f_seek_5_none.png")
        # b seek 5.
        self.menu_b_seek_5_normal_pixbuf = app_theme.get_pixbuf("screen/menu_b_seek_5_normal.png")
        self.menu_b_seek_5_hover_pixbuf = app_theme.get_pixbuf("screen/menu_b_seek_5_hover.png")
        self.menu_b_seek_5_none_pixbuf = app_theme.get_pixbuf("screen/menu_b_seek_5_none.png")
        # volume.
        self.menu_volume_normal_pixbuf = app_theme.get_pixbuf("screen/menu_volume_normal.png")
        self.menu_volume_hover_pixbuf = app_theme.get_pixbuf("screen/menu_volume_hover.png")
        self.menu_volume_none_pixbuf = app_theme.get_pixbuf("screen/menu_volume_none.png")
        # settin.
        self.menu_setting_normal_pixbuf = app_theme.get_pixbuf("screen/menu_setting_normal.png")
        self.menu_setting_hover_pixbuf = app_theme.get_pixbuf("screen/menu_setting_hover.png")
        self.menu_setting_none_pixbuf = app_theme.get_pixbuf("screen/menu_setting_none.png")
        # quit.
        self.menu_quit_normal_pixbuf = app_theme.get_pixbuf("screen/menu_quit_normal.png")
        self.menu_quit_hover_pixbuf = app_theme.get_pixbuf("screen/menu_quit_hover.png")
        self.menu_quit_none_pixbuf = app_theme.get_pixbuf("screen/menu_quit_none.png")
        # subtitle.
        self.menu_subtitle_normal_pixbuf = app_theme.get_pixbuf("screen/menu_subtitle_normal.png")
        self.menu_subtitle_hover_pixbuf = app_theme.get_pixbuf("screen/menu_subtitle_hover.png")
        self.menu_subtitle_none_pixbuf = app_theme.get_pixbuf("screen/menu_subtitle_none.png")        
        # play sequence pixbuf.
        self.play_sequence_select_normal_pixbuf = app_theme.get_pixbuf("screen/check_normal.png")
        self.play_sequence_select_hover_pixbuf = app_theme.get_pixbuf("screen/check_hover.png")
        self.play_sequence_select_none_pixbuf = app_theme.get_pixbuf("screen/check_none.png")
        # channel_select pixbuf.
        self.select_channel_normal_pixbuf = app_theme.get_pixbuf("screen/check_normal.png")
        self.select_channel_hover_pixbuf = app_theme.get_pixbuf("screen/check_hover.png")        
        self.select_channel_none_pixbuf = app_theme.get_pixbuf("screen/check_none.png")                
        # mute/add/sub volume pixbuf.
        self.mute_normal_pixbuf = app_theme.get_pixbuf("screen/menu_volume_menu_normal.png")
        self.mute_hover_pixbuf = app_theme.get_pixbuf("screen/menu_volume_menu_hover.png")
        self.mute_none_pixbuf = app_theme.get_pixbuf("screen/menu_volume_menu_none.png")                
        self.mute_volume_pixbuf = (self.mute_normal_pixbuf, self.mute_hover_pixbuf, self.mute_none_pixbuf)
        # add volume.
        self.add_volume_normal_pixbuf = app_theme.get_pixbuf("screen/menu_volume_add_normal.png")
        self.add_volume_hover_pixbuf = app_theme.get_pixbuf("screen/menu_volume_add_hover.png")
        self.add_volume_none_pixbuf = app_theme.get_pixbuf("screen/menu_volume_add_none.png")
        self.add_volume_pixbuf = (self.add_volume_normal_pixbuf, self.add_volume_hover_pixbuf, self.add_volume_none_pixbuf)
        # sub volume.
        self.sub_volume_normal_pixbuf = app_theme.get_pixbuf("screen/menu_volume_sub_normal.png")
        self.sub_volume_hover_pixbuf = app_theme.get_pixbuf("screen/menu_volume_sub_hover.png")
        self.sub_volume_none_pixbuf = app_theme.get_pixbuf("screen/menu_volume_sub_none.png")
        self.sub_volume_pixbuf = (self.sub_volume_normal_pixbuf, self.sub_volume_hover_pixbuf, self.sub_volume_none_pixbuf)        
        # down subtitle pixbuf.
        self.down_sub_title_bool = False
        self.down_sub_title_norma_pixbuf = app_theme.get_pixbuf("screen/check_normal.png")
        self.down_sub_title_hover_pixbuf = app_theme.get_pixbuf("screen/check_hover.png")
        self.down_sub_title_none_pixbuf = app_theme.get_pixbuf("screen/check_none.png")
        
        
    def __init_menus(self):
        self.config_gui      = None
        self.quit            = None
        self.init_user_guide = None
        ##############################################################
        self.file_menu = Menu([(None, _("Open File"), None),
                               (None, _("Open Directory"), None),
                               (None, _("Play Disc"), None)
                               ])
        self.play_state_menu = Menu([(None, _("Play (track)"), None),
                                     (None,  _("Default"), None),
                                     (None, _("Random"), None),
                                     (None, _("Repeat (track)"), None),
                                     (None, _("Repeat (playlist)"), None)]
                                    )                       
        self.play_menu = Menu([(None, _("Full Screen"), None),
                               (None, _("Normal Mode"), None),
                               (None, _("Compact Mode"), None),
                               (None, _("Previous"), None),
                               (None, _("Next"), None),
                               (None),
                               (None, _("Jump Forward"), None),
                               (None, _("Jump Backward"), None),
                               (None, _("Order"), self.play_state_menu),
                               ])
        self.video_menu = Menu([(None, _("Original"), None),
                                 (None,    "4:3",   None),
                                 (None,   "16:9",   None),
                                 (None,  "16:10",   None),
                                 (None, "1.85:1",   None),
                                 (None, "2.35:1",   None),
                                 (None),
                                 (None,  _("50%"),  None),
                                 (None,  _("100%"), None),
                                 (None,  _("150%"), None),
                                 (None,  _("200%"), None),
                                 ])  
        self.channel_select_menu = Menu([
                (None, _("Stereo"), None),
                (None,   _("Left"), None),
                (None,  _("Right"), None)
                ])
        self.audio_menu = Menu([(None, _("Channels"), self.channel_select_menu),
                                 (None),
                                 (None, _("Increase Volume"),  None),
                                 (None, _("Decrease Volume"),  None),
                                 (None, _("Mute/Unmute"), None),
                                 ])
        self.sort_menu = Menu([(None, _("Take Screenshot"), None),
                               (None, _("Open Screenshot Directory"), None),
                               (None, _("Set Screenshot Directory"), None)
                               ])
        self.format_menu = Menu([(None, _("Format conversion"), None),
                            (None, _("Task Manager"), None)
                            ])
        self.title_root_menu = Menu([
                                    (None, _("File"),  self.file_menu),
                                    (None, _("Play"),  self.play_menu),
                                    (None, _("Video"), self.video_menu),
                                    (None, _("Audio"), self.audio_menu),
                                    (None, _("Take Screenshots"), self.sort_menu),
                                    (None, _("Format conversion"), self.format_menu),
                                    (None, _("View New Features"), self.__menu_init_user_guide),
                                    (None, _("Preferences"), self.__menu_config_gui),
                                    (None),
                                    (None, _("Quit"), self.__menu_quit)
                                    ],
                                    True)
                                     
    def show_theme_menu(self, button): 
        # 显示主题上菜单.
        self.title_root_menu.show(
             get_widget_root_coordinate(button, WIDGET_POS_BOTTOM_LEFT),
             (button.get_allocation().width, 0)) 
                  
    def __menu_init_user_guide(self):
        if self.init_user_guide:
            self.init_user_guide()
                      
    def __menu_config_gui(self):
        if self.config_gui:    
            self.config_gui()
    
    def __menu_quit(self):
        if self.quit:
            self.quit()
            
                                        
