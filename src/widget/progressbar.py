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


from dtk.ui.theme import ui_theme
from dtk.ui.draw import draw_vlinear, draw_hlinear
from skin import app_theme
from color import color_hex_to_cairo
from draw  import draw_pixbuf
import gtk
import gobject



class ProgressBar(gtk.Button):
    __gsignals__ = {
        "value-changed" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,(float,)),
        }  
    def __init__(self):
        gtk.Button.__init__(self)
        self.__init_values()
        self.__init_events()
        self.set_size_request(-1, self.drag_pixbuf_height)

    def __init_values(self):
        self.color = ui_theme.get_color("scrolledbar")
        #
        self.drag_pixbuf = app_theme.get_pixbuf("progressbar/slide_block.png").get_pixbuf()
        self.drag_pixbuf_width = self.drag_pixbuf.get_width()
        self.drag_pixbuf_height = self.drag_pixbuf.get_height()
        #
        self.max_value = 100
        self.min_value = 0
        self.pos       = 0
        self.drag_show_check = False
        self.__move_check = False
        #

    def __init_events(self):
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.connect("motion-notify-event",  self.__motion_notify_event)
        self.connect("enter-notify-event",   self.__enter_notify_event)
        self.connect("leave-notify-event",   self.__leave_notify_event)
        self.connect("button-press-event",   self.__button_press_event)
        self.connect("button-release-event", self.__button_release_event)
        self.connect("expose-event",         self.__expose_event)

    def __motion_notify_event(self, widget, event):
        if self.__move_check:
            self.__event_pos(event)

    def __enter_notify_event(self, widget, event):
        self.drag_show_check = True

    def __leave_notify_event(self, widget, event):
        self.drag_show_check = False

    def __button_press_event(self, widget, event):
        print "__button_press_event....."
        self.__event_pos(event)
        self.__move_check = True

    def __event_pos(self, event):
        press_x = event.x
        width   = self.allocation.width
        value = press_x / width * self.max_value
        self.pos = value
        self.emit("value-changed", value)

    def __button_release_event(self, widget, event):
        self.__move_check = False

    def __expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        #
        self.__paint_progressbar(cr, rect)
        #
        return True

    def __paint_progressbar(self, cr, rect):
        # 画背景. draw background.
        bg_w = self.allocation.width
        bg_h = self.drag_pixbuf_height - 4 # 4(上下各留一像素,该死的设计师.)
        bg_x = rect.x
        bg_y = rect.y + rect.height/2 - bg_h/2
        bg_color = "#bebebe"
        bg_color_info = [(0.1, (bg_color, 1.0)),
                         (0.8, (bg_color, 1.0)),
                         (1.0, (bg_color, 0.8))]
        #draw_vlinear(cr, bg_x, bg_y, bg_w, bg_h, bg_color_info)
        draw_hlinear(cr, bg_x, bg_y, bg_w, bg_h, bg_color_info)
        ################################
        if self.get_sensitive(): # 
            d_value = float(rect.width) / self.max_value # 差值.
            # 画前景, 进度效果.
            fg_w = min(int(self.pos * d_value), int(self.max_value * d_value))
            fg_h = self.drag_pixbuf_height - 4 
            fg_x = rect.x
            fg_y = rect.y + rect.height/2 - fg_h/2
            fg_color = self.color.get_color()
            fg_color_info = [(0.1, (fg_color, 1.0)),
                             (0.75, (fg_color, 1.0)),
                             (1.0, (fg_color, 0.85))]
            #
            draw_hlinear(cr, fg_x, fg_y, fg_w, fg_h, fg_color_info)
            # 画拖动的点.
            if self.drag_show_check: # 是否显示拖动的点.
                drag_value = int(self.pos * d_value - self.drag_pixbuf_width/2)
                max_drag_value = int(self.max_value * d_value) - self.drag_pixbuf_width + 2
                min_drag_value = rect.x - 1
                # 防止拖动的点跑出可视区域.
                drag_x = max(min(drag_value, max_drag_value), min_drag_value)
                drag_y = rect.y + rect.height/2 - self.drag_pixbuf_height/2
                draw_pixbuf(cr, 
                            self.drag_pixbuf, 
                            drag_x, 
                            drag_y)

    def set_max_value(self, value):
        self.max_value = value
        self.queue_draw()

    def set_pos(self, pos):
        self.pos = pos
        #self.queue_draw()



gobject.type_register(ProgressBar)


