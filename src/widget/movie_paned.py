#! /usr/bin/ python
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


import gtk
from gtk import gdk
import gobject
from color import alpha_color_hex_to_cairo
from draw import draw_text
from skin import app_theme




class Paned(gtk.Bin):
    def __init__(self):
        gtk.Bin.__init__(self)
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.__init_values()

    def __init_values(self):
        self.screen = None
        self.alpha = 1.0
        self.handle_alpha = 1.0
        self.top_win_h = 25
        self.bottom_win_h = 50
        self.top_win_show_check = False
        self.bottom_win_show_check = False
        #
        self.top_child = None
        self.bottom_child = None
        self.__child1 = None
        self.__child2 = None
        self.__child2_move_width = 0 #175
        self.__child2_min_width  = 175
        self.save_move_width   = 0
        self.move_check = False # 是否移动paned.
        self.show_check = False # 是否显示handle图片.
        #
        self.__handle = None
        self.__handle_pos_x = self.__child2_move_width
        self.__handle_pos_y = 0
        self.__handle_pos_w = 6
        self.__handle_pos_h = self.allocation.height
        #
        self.paint_bottom_window = self.__paint_bottom_window
        #
        self.in_pixbuf = app_theme.get_pixbuf("paned/in.png").get_pixbuf()
        self.out_pixbuf = app_theme.get_pixbuf("paned/out.png").get_pixbuf()

    def do_realize(self):
        gtk.Bin.do_realize(self)
        self.set_realized(True)
        self.allocation.x = 0
        self.allocation.y = 0
        self.window = gdk.Window(
            self.get_parent_window(),
            window_type=gdk.WINDOW_CHILD,
            x=self.allocation.x,
            y=self.allocation.y,
            width=self.allocation.width,
            height=self.allocation.height,
            colormap=self.get_colormap(),
            wclass=gdk.INPUT_OUTPUT,
            visual=self.get_visual(),
            event_mask=(self.get_events() 
                      | gdk.EXPOSURE_MASK
                      | gdk.BUTTON_MOTION_MASK
                      | gdk.ENTER_NOTIFY_MASK
                      | gdk.LEAVE_NOTIFY_MASK
                      | gdk.POINTER_MOTION_HINT_MASK
                      | gdk.BUTTON_PRESS_MASK
                      ))
        self.window.set_user_data(self)
        #self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.__init_handle_window()
        self.__init_top_window()
        self.__init_bottom_window()
        if self.__child1:
            self.__child1.set_parent_window(self.window)
        if self.__child2:
            self.__child2.set_parent_window(self.window)
        self.queue_resize()

    def __init_handle_window(self):
        self.__handle = gdk.Window(
            self.window,
            window_type=gdk.WINDOW_CHILD,
            wclass=gdk.INPUT_ONLY,
            x=self.__handle_pos_x,
            y=self.__handle_pos_y,
            width=self.__handle_pos_w, 
            height=self.allocation.height,
            event_mask=(self.get_events() 
                      | gdk.EXPOSURE_MASK
                      | gdk.BUTTON_PRESS_MASK
                      | gdk.BUTTON_RELEASE_MASK
                      | gdk.ENTER_NOTIFY_MASK
                      | gdk.LEAVE_NOTIFY_MASK
                      | gdk.POINTER_MOTION_MASK
                      | gdk.POINTER_MOTION_HINT_MASK
                      ))
        self.__handle.set_user_data(self)
        self.style.set_background(self.__handle, gtk.STATE_NORMAL)
        if (self.__child1 and self.__child1.get_visible() and 
            self.__child2 and self.__child2.get_visible()):
            self.__handle.show()

    def __init_top_window(self):
        self.top_window = gdk.Window(
                self.window,
                window_type=gdk.WINDOW_CHILD,
                wclass=gdk.INPUT_OUTPUT,
                x=0,
                y=0,
                width=self.allocation.width, 
                height=self.top_win_h,
                event_mask=(self.get_events() 
                          | gdk.EXPOSURE_MASK
                          | gdk.BUTTON_PRESS_MASK
                          | gdk.BUTTON_RELEASE_MASK
                          | gdk.ENTER_NOTIFY_MASK
                          | gdk.LEAVE_NOTIFY_MASK
                          | gdk.POINTER_MOTION_MASK
                          | gdk.POINTER_MOTION_HINT_MASK
                          ))
        self.top_window.set_user_data(self)
        #self.style.set_background(self.top_window, gtk.STATE_NORMAL)
        if self.top_child:
            self.top_child.set_parent_window(self.top_window)

    def __init_bottom_window(self):
        self.bottom_window = gdk.Window(
                self.window,
                window_type=gdk.WINDOW_CHILD,
                wclass=gdk.INPUT_OUTPUT,
                x=0,
                y=0 + self.allocation.height - self.bottom_win_h,
                width=self.allocation.width, 
                height=self.bottom_win_h,
                event_mask=(self.get_events() 
                          | gdk.EXPOSURE_MASK
                          | gdk.BUTTON_PRESS_MASK
                          | gdk.BUTTON_RELEASE_MASK
                          | gdk.ENTER_NOTIFY_MASK
                          | gdk.LEAVE_NOTIFY_MASK
                          | gdk.POINTER_MOTION_MASK
                          | gdk.POINTER_MOTION_HINT_MASK
                          ))
        self.bottom_window.set_user_data(self)
        #self.style.set_background(self.bottom_window, gtk.STATE_NORMAL)
        if self.bottom_child:
            self.bottom_child.set_parent_window(self.bottom_window)
        
    def do_unrealize(self):
        gtk.Bin.do_unrealize(self)

    def do_map(self):
        gtk.Bin.do_map(self)
        self.set_flags(gtk.MAPPED)
        self.__handle.show()
        self.window.show()
        self.top_window.hide()
        self.bottom_window.hide()

    def do_unmap(self):
        gtk.Bin.do_unmap(self)
        self.__handle.hide()
        
    def do_expose_event(self, e):
        gtk.Bin.do_expose_event(self, e)
        #
        self.__paint_top_window(e)
        if e.window == self.bottom_window:
            self.paint_bottom_window(e)
            gtk.Bin.do_expose_event(self, e)
            return False
        self.__paint_screen(e)
        self.__paint_handle(e)
        return False

    def __paint_top_window(self, e):
        if e.window == self.top_window:
            top_rect = self.top_window.get_size()
            cr = self.top_window.cairo_create()
            cr.set_source_rgba(*alpha_color_hex_to_cairo(("#ebebeb", 0.1)))
            cr.rectangle(0, 0, top_rect[0], top_rect[1])
            cr.fill()
            return False

    def __paint_bottom_window(self, e):
        bottom_rect = self.bottom_window.get_size()
        cr = self.bottom_window.cairo_create()
        cr.set_source_rgba(*alpha_color_hex_to_cairo(("#ebebeb", 0.1)))
        cr.rectangle(0, 0, bottom_rect[0], bottom_rect[1])
        cr.fill()


    def __paint_screen(self, e):
        if self.screen:
            cr = self.window.cairo_create()
            cr.set_source_pixmap(self.screen.window, *self.screen.window.get_position())
            cr.paint_with_alpha(self.alpha)
            # 画提示信息.
            #if self.toptip_text:
            if False: # 预留功能. [画在屏幕上的提示信息].
                draw_text(cr, 
                          self.toptip_text, 
                          self.toptip_x,
                          self.toptip_y,
                          text_color=self.toptip_color,
                          text_size=self.toptip_size)

    def __paint_handle(self, e):
        if self.show_check:
            cr = self.window.cairo_create()
            if self.get_move_width() == 0:
                pixbuf = self.out_pixbuf
            else:
                pixbuf = self.in_pixbuf
            self.__handle_pos_h = pixbuf.get_height()
            #
            y = 0 + self.allocation.height/2 - self.__handle_pos_h/2
            cr.set_source_pixbuf(pixbuf, 
                                 self.__handle_pos_x - self.__handle_pos_w - 1, 
                                 y)
            cr.paint_with_alpha(self.handle_alpha)

    def do_motion_notify_event(self, e):
        #print "event.x:", e.x
        if e.window == self.__handle:
            self.show_check = True
            self.queue_draw()
            return False
        if e.window == self.window:
            #
            if self.__in_top_win(e):
                if e.window != self.bottom_window:
                    self.top_window.show()
                    self.top_win_show_check = True
            else:
                self.top_window.hide()
                self.top_win_show_check = False
            #
            '''
            if self.__in_bottom_win(e):
                self.bottom_window.show()
                self.bottom_win_show_check = True
            '''
            #
        else:
            self.show_check = False
            self.queue_draw()
        return False

    def do_button_press_event(self, e):
        #print "do_button_press_event..."
        return False

    def do_button_release_event(self, e):
        #print "do_button_release_event..."
        return False

    def do_enter_notify_event(self, e):
        if e.window == self.__handle:
            self.show_check = True
            self.queue_draw()
            self.__handle.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))

    def do_leave_notify_event(self, e):
        if e.window == self.__handle:
            self.show_check = False
            self.queue_draw()
        elif e.window == self.top_window:
            if not self.__in_top_win(e):
                self.top_window.hide()
                self.top_win_show_check = False
        '''
        elif e.window == self.bottom_window:
            self.bottom_window.hide()
            self.bottom_win_show_check = False
        '''

    def __in_top_win(self, e):
        min_y = 0
        max_y = 0 + self.top_win_h
        min_x = 0
        max_x = 0 + self.top_window.get_size()[0]
        return (min_y <= int(e.y) <= max_y and min_x <= int(e.x) <= max_x)

    def __in_bottom_win(self, e):
        min_x = 0
        max_x = 0 + self.top_window.get_size()[0]
        min_y = 0 + self.allocation.height - self.bottom_win_h
        max_y = 0 + self.allocation.height 
        return (min_y <= int(e.y) <= max_y and min_x <= int(e.x) <= max_x)

    def do_size_allocate(self, allocation):
        self.allocation = allocation
        self.allocation.x = 0
        self.allocation.y = 0
        # 
        self.set_all_size()

    def set_all_size(self):
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*self.allocation)
        # 左边的控件.
        if self.__child1:
            child1_allocation = gdk.Rectangle()
            child1_allocation.x = 0 
            child1_allocation.y = 0 
            child1_allocation.width = self.allocation.width - self.__child2_move_width
            child1_allocation.height = self.allocation.height
            self.__child1.size_allocate(child1_allocation)
            # top and bottom window move resize.
            if self.flags() & gtk.REALIZED:
                self.top_window.move_resize(0, 0, 
                                            child1_allocation.width, 
                                            self.top_win_h)
                if self.top_child:
                    top_child_allocation = gdk.Rectangle()
                    top_child_allocation.x = 0
                    top_child_allocation.y = 0
                    top_child_allocation.width = child1_allocation.width
                    top_child_allocation.height = self.top_win_h
                    self.top_child.size_allocate(top_child_allocation)
                self.bottom_window.move_resize(0, 
                                               0 + self.allocation.height - self.bottom_win_h, 
                                               child1_allocation.width, 
                                               self.bottom_win_h)
                if self.bottom_child:
                    bottom_child_allocation = gdk.Rectangle()
                    bottom_child_allocation.x = 0
                    bottom_child_allocation.y = 0
                    bottom_child_allocation.width = child1_allocation.width
                    bottom_child_allocation.height = self.bottom_win_h
                    self.bottom_child.size_allocate(bottom_child_allocation)
        # 右边的控件.
        if self.__child2:
            child2_allocation = gdk.Rectangle()
            child2_allocation.width = self.__child2_move_width
            child2_allocation.height = self.allocation.height
            child2_allocation.x = self.allocation.width - self.__child2_move_width 
            child2_allocation.y = 0
            self.__child2.size_allocate(child2_allocation)
        self.__handle_pos_x = child2_allocation.x
        self.__handle_pos_y = child2_allocation.y
        if self.__handle:
            self.__handle.move_resize(
                    self.__handle_pos_x - self.__handle_pos_w,
                    self.__handle_pos_y,
                    self.__handle_pos_w,
                    self.allocation.height
                    )

    def do_forall(self, include_internals, callback, data):
        if self.top_child:
            callback(self.top_child, data)
        if self.bottom_child:
            callback(self.bottom_child, data)
        if self.child:
            callback(self.child, data)
        if self.__child1:
            callback(self.__child1, data)
        if self.__child2:
            callback(self.__child2, data)

    def do_size_request(self, req):
        if self.top_child:
            self.top_child.size_request()
        if self.bottom_child:
            self.bottom_child.size_request()
        if self.child:
            self.child.size_request()
        if self.__child1:
            self.__child1.size_request()
        if self.__child2:
            self.__child2.size_request()

    def do_add(self, widget):
        gtk.Bin.do_add(self, widget)

    def do_remove(self, widget):
        widget.unparent()

    ####################################
    def add1(self, widget):
        self.__child1 = widget
        self.__child1.set_parent(self)

    def add2(self, widget):
        self.__child2 = widget
        self.__child2.set_parent(self)

    def add_top_widget(self, widget):
        self.top_child = widget
        self.top_child.set_parent(self)

    def add_bottom_widget(self, widget):
        self.bottom_child = widget
        self.bottom_child.set_parent(self)
    
    def set_min_width(self, width=150):
        self.__child2_min_width = width

    def set_move_width(self, width):
        self.__child2_move_width = max(width, self.__child2_min_width)

    def get_move_width(self):
        return self.__child2_move_width

    def set_jmp_end(self):
        self.save_move_width = self.__child2_move_width
        self.__child2_move_width = 0

    def set_jmp_start(self):
        self.set_move_width(self.get_move_width())

    def set_move_check(self, move_check): # 是否支持移动.
        self.move_check = move_check

    def show_bottom_toolbar(self):
        self.bottom_win_show_check = True

    def hide_bottom_toolbar(self):
        self.bottom_win_show_check = False

    def set_visible_handle(self, check):
        if check:
            self.__handle.show()
        else:
            self.__handle.hide()

gobject.type_register(Paned) 



if __name__ == "__main__":
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(500, 500)
    paned = Paned()
    #
    #movie_win  = MovieWindow()
    
    scroll_win = gtk.ScrolledWindow()
    scroll_win.add_with_viewport(gtk.Button("fjdksf"))
    #
    movie_screen_ali    = gtk.Alignment(0, 0, 1, 1)
    movie_screen = gtk.DrawingArea()
    #movie_screen.
    #movie_screen.unset_flags(gtk.DOUBLE_BUFFERED)
    movie_screen_ali.add(movie_screen)
    #
    #movie_win.add(movie_screen_ali)
    paned.screen = movie_screen
    paned.add1(movie_screen_ali)
    #paned.add1(movie_win)
    #paned.add1(gtk.Button("fdjskf"))
    paned.add2(scroll_win)
    #
    win.add(paned)
    win.show_all()
    movie_screen.realize()
    movie_screen.window.set_composited(True)
    print movie_screen.window.xid
    gtk.main()


