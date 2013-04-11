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


from utils import get_match_parent
import gtk
from gtk import gdk
import gobject


class TreeViewBase(gtk.Container):
    def __init__(self):
        gtk.Container.__init__(self)
        self.__init_values()

    def __init_values(self):
        self.nodes = Nodes()
        self.nodes.connect("update-data", self.__nodes_update_data_event)
        #self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        #
        self.header_height = 35
        self.__init_values_columns()
        self.set_can_focus(True)
        self.set_redraw_on_allocate(False)

    def __init_values_columns(self):
        self.columns = []

    def __nodes_update_data_event(self, nodes):
        print "__nodes_update_data_event..."
        
    def do_map(self):
        print "do..map.."
        gtk.Container.do_map(self)
        self.set_flags(gtk.MAPPED)
        for child in self.children():
            print "do..map child:", child
        #
        self.bin_window.show()
        self.header_window.show()
        self.window.show()

    def do_umap(self):
        print "do_map:"
        gtk.Container.do_umap(self)
        self.window.hide()
        self.bin_window.hide()
        self.header_window.hide()

    def do_realize(self):
        print "do_realize..."
        self.set_realized(True)
        #
        self.__init_window()
        self.__init_bin_window()
        self.__init_header_window()
        #
        #
        self.__init_children()
        #
        self.scroll_win = get_match_parent(self, ["ScrolledWindow"])
        self.hadjustment = self.scroll_win.get_hadjustment()
        self.vadjustment = self.scroll_win.get_vadjustment()
        self.hadjustment.connect("value-changed", self.__list_view_adjustments_changed)
        self.vadjustment.connect("value-changed", self.__list_view_adjustments_changed)
        self.queue_resize()

    def __list_view_adjustments_changed(self, adjustments):
        self.header_window.move(0, int(self.vadjustment.value))
        self.bin_window.move(0, int(self.vadjustment.value))
        #
        self.header_window.process_updates(True)
        self.bin_window.process_updates(True)

    def __init_window(self):
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
            event_mask=gtk.gdk.VISIBILITY_NOTIFY
            )
        self.window.set_user_data(self)
        self.window.set_back_pixmap(None, False)

    def __init_bin_window(self):
        self.bin_window = gdk.Window(
                self.window, 
                window_type=gdk.WINDOW_CHILD,
                x=0,
                y=self.header_height,
                width=self.allocation.width,
                height=self.allocation.height,
                colormap=self.get_colormap(),
                wclass=gdk.INPUT_OUTPUT,
                visual=self.get_visual(),
                event_mask=(self.get_events() 
                          | gdk.EXPOSURE_MASK
                          | gdk.SCROLL_MASK
                          | gdk.POINTER_MOTION_MASK
                          | gdk.ENTER_NOTIFY_MASK
                          | gdk.LEAVE_NOTIFY_MASK
                          | gdk.BUTTON_PRESS_MASK
                          | gdk.BUTTON_RELEASE_MASK
                          ))
        self.bin_window.set_user_data(self)
        self.style.set_background(self.bin_window, gtk.STATE_NORMAL)

    def __init_header_window(self):
        # 标题头窗口.
        self.header_window = gdk.Window(
                self.window,
                window_type=gdk.WINDOW_CHILD,
                x=0,
                y=0,
                width=self.allocation.width,
                height=self.header_height,
                colormap=self.get_colormap(),
                wclass=gdk.INPUT_OUTPUT,
                visual=self.get_visual(),
                event_mask=(self.get_events() 
                          | gdk.EXPOSURE_MASK
                          | gdk.SCROLL_MASK
                          | gdk.ENTER_NOTIFY_MASK
                          | gdk.LEAVE_NOTIFY_MASK
                          | gdk.BUTTON_PRESS_MASK
                          | gdk.BUTTON_RELEASE_MASK
                          | gdk.KEY_PRESS_MASK
                          | gdk.KEY_RELEASE_MASK
                          ))
        self.header_window.set_user_data(self)
        self.style.set_background(self.header_window, gtk.STATE_NORMAL)

    def __init_children(self):
        for child in self.children():
            print "child:", child

    def do_unrealize(self):
        #
        self.bin_window.set_user_data(None)
        self.bin_window.destroy()
        self.bin_window = None
        #
        self.header_window.set_user_data(None)
        self.header_window.destroy()
        self.header_window = None
        # 

    def do_expose_event(self, e):
        gtk.Container.do_expose_event(self, e)
        #
        if e.window == self.bin_window:
            self.__tree_view_bin_expose(e)
        elif e.window == self.header_window:
            header_size = self.header_window.get_size()
            cr = self.header_window.cairo_create()
            cr.set_source_rgba(1, 0, 0, 1)
            cr.rectangle(0, 0, header_size[0], header_size[1])
            cr.fill()
            return False
        elif e.window == self.drag_window:
            pass
        return True

    def __tree_view_bin_expose(self, e):
        bin_size = self.bin_window.get_size()
        cr = self.bin_window.cairo_create()
        cr.set_source_rgba(0, 0, 1, 1)
        cr.rectangle(0, 0, bin_size[0], bin_size[1])
        cr.fill()
        return False

    def do_motion_notify_event(self, e):
        print "do--mo--no--ev"
        return False

    def do_button_press_event(self, e):
        print "do_button_press_event..."
        if e.window == self.bin_window:
            if e.button == 1:
                self.grab_add()
            if e.button == 1 and e.type == gtk.gdk.BUTTON_PRESS:
                print "double..."
            return True
            
        return False

    def do_button_release_event(self, e):
        #print "do_button_release_event..."
        return False

    def do_enter_notify_event(self, e):
        return False

    def do_leave_notify_event(self, e):
        return False

    def do_size_request(self, req):
        pass

    def do_size_allocate(self, allocation):
        print "do_size_allocate...", allocation
        gtk.Container.do_size_allocate(self, allocation)
        for child in self.children():
            allocation = gdk.Rectangle()
            allocation.x  = child.x
            allocation.y  = child.y
            allocation.width = child.width
            allocation.height = child.height
        #
        # self.window , self.header_window, self.bin_window
        if self.get_realized():
            self.window.move_resize(
                    self.allocation.x,
                    self.allocation.y,
                    self.allocation.width,
                    self.allocation.height)
            self.header_window.move_resize(
                    0, 
                    0,
                    self.allocation.width,
                    self.header_height)
            self.bin_window.move_resize(
                    0,
                    self.header_height,
                    self.allocation.width,
                    self.allocation.height)

    def do_destroy(self):
        print "do_destroy..."


gobject.type_register(TreeViewBase)



class Nodes(list):
    def __init__(self):
        list.__init__(self)
        self.__init_values()


    def __init_values(self):
        self.__function_point = None
        self.text = ""

    def add(self, list):
        nodes = Nodes()
        nodes.connect("update-data", self.__nodes_update_data_event)
        nodes.text = list
        self.append(nodes)
        self.emit()

    def __nodes_update_data_event(self, nodes):
        self.emit()

    def add_range(self, lists):
        self.__add_range_function(lists)
        self.emit()

    def __add_range_function(self, lists):
        pass

    def connect(self, event_name, function_point):
        if event_name == "update-data":
            self.__function_point = function_point

    def emit(self):
        if self.__function_point:
            self.__function_point(self)
        


if __name__ == "__main__":
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(300, 300)
    treeview_base = TreeViewBase()
    # root 节点.
    treeview_base.nodes.text = "root"
    # root1.
    treeview_base.nodes.add("root1")
    treeview_base.nodes[0].add("root1-1")
    treeview_base.nodes[0].add("root1-2")
    treeview_base.nodes[0].add("root1-3")
    treeview_base.nodes[0][0].add("root1-1-1")
    treeview_base.nodes[0][0].add("root1-1-2")
    print treeview_base.nodes[0][0][0].text
    #########################################
    treeview_base.set_size_request(1500, 1500)
    scroll_win = gtk.ScrolledWindow()
    scroll_win.add_with_viewport(treeview_base)
    win.add(scroll_win)
    win.show_all()
    gtk.main()



