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

from skin import app_theme
from dtk.ui.frame import HorizontalFrame
from dtk.ui.volume_button import VolumeButton
from show_time import ShowTime
from play_control_panel import PlayControlPanel

import gtk

class BottomToolBar(object):            
    def __init__(self):
        self.vbox = gtk.VBox()
        
        self.hbox = gtk.HBox()
        # hbox add child widget.
        self.show_time_hframe = HorizontalFrame()
        self.show_time = ShowTime()
        self.show_time.time_font1 = "00:00:00"
        self.show_time.time_font2 = "00:00:00 / "
        self.show_time.set_time_font(self.show_time.time_font2, self.show_time.time_font1)
        self.show_time_hframe.add(self.show_time.time_box)
        show_time_padding_widht = 110
        show_time_padding_height = -1
        self.show_time.time_box.set_size_request(
            show_time_padding_widht, 
            show_time_padding_height
            )
        self.show_time_hframe.set(0, 0, 1, 1)
        self.show_time_hframe.set_padding(2, 0, 10, 40)
        
        self.play_control_panel = PlayControlPanel()      
        self.play_control_panel_hframe = self.play_control_panel.hbox_hframe
        self.play_control_panel_hframe.set(0, 0, 0, 0)
        self.play_control_panel_hframe.set_padding(0, 0, 0, 0)
        
        self.volume_hframe = HorizontalFrame()
        self.volume_button = VolumeButton(press_emit_bool = True,
                 zero_volume_normal_pixbuf = app_theme.get_pixbuf("volume_button/zero_normal.png"),
                 zero_volume_hover_pixbuf = app_theme.get_pixbuf("volume_button/zero_hover.png"),
                 zero_volume_press_pixbuf = app_theme.get_pixbuf("volume_button/zero_press.png"),
                 min_volume_normal_pixbuf = app_theme.get_pixbuf("volume_button/lower_normal.png"),
                 min_volume_hover_pixbuf = app_theme.get_pixbuf("volume_button/lower_hover.png"),
                 min_volume_press_pixbuf = app_theme.get_pixbuf("volume_button/lower_press.png"),
                 mid_volume_normal_pixbuf = app_theme.get_pixbuf("volume_button/middle_normal.png"),
                 mid_volume_hover_pixbuf = app_theme.get_pixbuf("volume_button/middle_hover.png"),
                 mid_volume_press_pixbuf = app_theme.get_pixbuf("volume_button/middle_press.png"),
                 max_volume_normal_pixbuf = app_theme.get_pixbuf("volume_button/high_normal.png"),
                 max_volume_hover_pixbuf = app_theme.get_pixbuf("volume_button/high_hover.png"),
                 max_volume_press_pixbuf = app_theme.get_pixbuf("volume_button/high_press.png"),
                 mute_volume_normal_pixbuf = app_theme.get_pixbuf("volume_button/mute_normal.png"),
                 mute_volume_hover_pixbuf = app_theme.get_pixbuf("volume_button/mute_hover.png"),
                 mute_volume_press_pixbuf = app_theme.get_pixbuf("volume_button/mute_press.png")
               )
        volume_button_padding_width = 120
        volume_button_padding_height = 50
        self.volume_button.set_size_request(
            volume_button_padding_width, 
            volume_button_padding_height
            )
        self.volume_hframe.add(self.volume_button)
        self.volume_hframe.set(1, 0, 0, 0)
        self.volume_hframe.set_padding(0, 0, 0, 0)
        
        
        self.hbox.pack_start(self.show_time_hframe, True, True)
        self.hbox.pack_start(self.play_control_panel.hbox_hframe, True, True)
        self.hbox.pack_start(self.volume_hframe, False, False)
        label = gtk.Label()
        label.set_size_request(10, 1)
        self.hbox.pack_start(label, False, False)
        
        self.vbox.pack_start(self.hbox, True, True)
                
                
if __name__ == "__main__":    
            
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    tb = BottomToolBar()
    win.connect("destroy", gtk.main_quit)
    win.add(tb.vbox)
    win.add_events(gtk.gdk.ALL_EVENTS_MASK)
    
    win.show_all()
    gtk.main()
