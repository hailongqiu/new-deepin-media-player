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

class MediaPlayFun(object):
    def __init__(self, this):
        self.this = this
        self.__init_values()
        self.__init_ldmp_values()

    def __init_values(self):
        self.bottom_toolbar = self.this.gui.bottom_toolbar
        self.bottom_toolbar.progressbar.connect("value-changed", self.__bottom_toolbar_pb_value_changed)
        #self.play_control_panel = 
        #self.volume_button = 
        #self.bottom_toolbar.stop_button
        self.__init_bottom_toolbar()
        #
        self.ldmp = self.this.ldmp
        self.play_list = self.this.play_list
        self.play_list.set_items_index(self.this.gui.play_list_view.list_view.items[3])

    def __bottom_toolbar_pb_value_changed(self, pb, value):
        print ".......", value
        self.ldmp.seek(value)

    def __init_bottom_toolbar(self):
        self.bottom_toolbar.play_control_panel.stop_button.connect("clicked",  self.__bottom_toolbar_stop_button_clicked)
        self.bottom_toolbar.play_control_panel.start_button.connect("clicked", self.__bottom_toolbar_start_button_clicked)

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
    ## ldmp.
    def ldmp_get_time_pos(self, ldmp, pos, time):
        self.__set_pos_time(time)
        self.bottom_toolbar.progressbar.set_pos(pos)

    def ldmp_get_time_length(self, ldmp, length, time):    
        self.__set_length_time(time)
        self.bottom_toolbar.progressbar.set_max_value(length)

    def __set_pos_time(self, time):
        self.__pos = str(time) + " / "
        self.bottom_toolbar.show_time.set_time_font(self.__pos, self.__length)

    def __set_length_time(self, time):
        self.__length = str(time)
        self.bottom_toolbar.show_time.set_time_font(self.__pos, self.__length)





