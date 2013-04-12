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
from utils import propagate_expose
import gtk
from gtk import gdk
import gobject
import random


class TreeViewChild(object):
    widget = None
    x = 0
    y = 0 
    w = 80
    h = 40

class TreeViewBase(gtk.Container):
    def __init__(self):
        gtk.Container.__init__(self)
        self.__init_values()

    def __init_values(self):
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        #
        self.header_height = 35
        self.node_height = 35
        self.children = []
        self.nodes = Nodes()
        self.nodes.connect("update-data", self.__nodes_update_data_event)
        self.__init_values_columns()

    def __nodes_update_data_event(self, nodes):
        print "__nodes_update_data_event..."

    def __init_values_columns(self):
        self.columns = []
        
    def do_map(self):
        print "do..map.."
        gtk.Container.do_map(self)
        self.set_flags(gtk.MAPPED)
        #
        self.window.show()

    def do_umap(self):
        print "do_map:"
        gtk.Container.do_umap(self)
        self.window.hide()

    def do_realize(self):
        print "do_realize..."
        self.set_realized(True)
        #
        self.__init_window()
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
        pass

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
            event_mask=(self.get_events() 
            | gtk.gdk.VISIBILITY_NOTIFY
            | gdk.EXPOSURE_MASK
            | gdk.SCROLL_MASK
            | gdk.POINTER_MOTION_MASK
            | gdk.ENTER_NOTIFY_MASK
            | gdk.LEAVE_NOTIFY_MASK
            | gdk.BUTTON_PRESS_MASK
            | gdk.BUTTON_RELEASE_MASK
            | gdk.KEY_PRESS_MASK
            | gdk.KEY_RELEASE_MASK
            ))
        self.window.set_user_data(self)
        self.style.set_background(self.window, gtk.STATE_NORMAL)


    def __init_children(self):
        for child in self.children:
            print "child:", child.widget.set_parent_window(self.window)

    def do_unrealize(self):
        #
        pass

    def do_expose_event(self, e):
        gtk.Container.do_expose_event(self, e)
        if e.window == self.window:
            cr = self.window.cairo_create()
            cr.set_source_rgba(0, 0, 1, 0.1)
            cr.rectangle(0, 0 + self.index * self.node_height, self.allocation.width, self.node_height)
            cr.fill()
        #propagate_expose(self, e)
        #
        return False

    def do_motion_notify_event(self, e):
        print "do--mo--no--ev", e.x
        if e.window == self.window:
            self.index = int(e.y) / self.node_height
            self.queue_draw()
        return False

    def do_button_press_event(self, e):
        print "do_button_press_event..."
        return False

    def do_button_release_event(self, e):
        print "do_button_release_event..."
        return False

    def do_enter_notify_event(self, e):
        print "do_enter_notify_event..."
        return False

    def do_leave_notify_event(self, e):
        print "do_leave_notify_event..."
        return False

    def do_size_request(self, req):
        for child in self.children:
            child.widget.size_request()

    def do_size_allocate(self, allocation):
        print "do_size_allocate..."
        gtk.Container.do_size_allocate(self, allocation)
        for child in self.children:
            allocation = gdk.Rectangle()
            allocation.x  = child.x
            allocation.y  = child.y
            allocation.width = child.w 
            allocation.height = child.h 
            child.widget.size_allocate(allocation)
        #
        if self.get_realized():
            self.window.move_resize(
                    self.allocation.x,
                    self.allocation.y,
                    self.allocation.width,
                    self.allocation.height)

    def do_destroy(self):
        print "do_destroy..."

    def do_forall(self, include_internals, callback, data):
        for child in self.children:
            callback(child.widget, data)

    def add_widget(self, child, x=0, y=0, w=0, h=0):
        child.set_parent(self)
        tree_view_child = TreeViewChild()
        tree_view_child.widget = child
        tree_view_child.x = x
        tree_view_child.y = y
        tree_view_child.w = max(w, 80)
        tree_view_child.h = max(h, self.node_height)
        self.children.append(tree_view_child)

gobject.type_register(TreeViewBase)



class Nodes(list):
    def __init__(self):
        list.__init__(self)
        self.this = None
        self.__function_point = None

    def add(self, text):
        node = Node()
        node.text = text
        node.parent = self
        if self.this:
            node.leave  = self.this.leave + 1
        node.connect("update-data", self.__node_update_data_event)
        self.append(node)
        self.emit()
        return node

    def __node_update_data_event(self, node):
        self.emit()

    def connect(self, event_name, function_point):
        if event_name == "update-data":
            self.__function_point = function_point

    def emit(self):
        if self.__function_point:
            self.__function_point(self)

class Node(object):
    def __init__(self):
        self.__function_point = None
        self.text  = ""
        self.children = []
        #
        self.nodes = Nodes()
        self.nodes.this = self
        self.nodes.connect("update-data", self.__nodes_update_data_event)
        #
        self.parent = None # 获取当前树节点的夫节点.
        self.leave  = 0    # 树的深度,不懂的看数据结构.
        self.__last_node  = []   # 获取最后一个子树节点.
        self.__first_node = []   # 获取树节点集合中的第一个子树节点.
        self.__next_node  = []   # 获取下一个同级节点.
        self.__prev_node  = []   # 获取上一个同级节点.
        self.__index      = None # 获取树节点在树节点集合中的位置.
        ####################
        self.is_editing  = False # 是否可编辑状态.
        self.is_expanded = False # 是否展开状态.
        self.is_selected = False # 是否选中状态.
        self.is_visible  = False # 是否可见.
        self.node_font   = None  # 字体.
        self.image       = None
        self.next_visible_node = None # 获取下一个可见树节点.


    def __nodes_update_data_event(self, nodes):
        self.emit()

    def connect(self, event_name, function_point):
        if event_name == "update-data":
            self.__function_point = function_point

    def emit(self):
        if self.__function_point:
            self.__function_point(self)

    @property
    def last_node(self):
    # 获取最后一个子树节点.
        return self.__last_node

    @last_node.getter
    def last_node(self):
        if self.nodes == []:
            return None
        else: 
            return self.nodes[len(self.nodes)-1]

    @property
    def first_node(self):
    # 获取树节点集合中的第一个子树节点.
        return self.__first_node

    @first_node.getter
    def first_node(self):
        if self.nodes == []:
            return None
        else: 
            return self.nodes[0]

    @property
    def prev_node(self):
        return self.__prev_node
    
    @prev_node.getter
    def prev_node(self):
        # 获取上一个同级节点.
        if self.parent:
            index = self.parent.index(self)
            print "prev index:", index
            if index:
                node = self.parent[index - 1]
                self.__prev_node = node
                return self.__prev_node
        return None

    @property
    def next_node(self):
        # 获取下一个同级节点.
        return self.__next_node

    @next_node.getter
    def next_node(self):
        if self.parent:
            index = self.parent.index(self)
            print "next index:", index
            if index < len(self.parent) - 1:
                node = self.parent[index + 1]
                self.__next_node = node
                return self.__next_node
        return None

    @next_node.deleter
    def next_node(self):
        del self.__next_node

    @property
    def index(self):
        return self.__index

    @index.getter
    def index(self):
        if self.parent:
            _index = self.parent.index(self) 
            return _index
        return None




if __name__ == "__main__":
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(300, 300)
    treeview_base = TreeViewBase()
    treeview_base.add_widget(gtk.Button("fjkdsf"))
    treeview_base.add_widget(gtk.Button("fjkdsf"))
    treeview_base.add_widget(gtk.Button("fjkdsf"))
    treeview_base.add_widget(gtk.Entry(), x=0, y=35)
    treeview_base.add_widget(gtk.CheckButton(label="fjdskf"), x=100, y=35)
    treeview_base.add_widget(gtk.CheckButton(label="fjdskf"), x=180, y=35)
    treeview_base.add_widget(gtk.CheckButton(label="fjdskf"), x=0, y=35*2)
    test_combo = gtk.combo_box_new_text()
    test_combo.append_text("option1 ")
    test_combo.append_text("option1 ")
    test_combo.append_text("option1 ")
    test_combo.append_text("option1 ")
    test_widget = gtk.HScale()
    test_widget.set_range(0, 100)
    test_image = gtk.Image()
    test_image.set_from_file("logo.png")
    treeview_base.add_widget(test_combo, x=100, y=35*2)
    treeview_base.add_widget(test_widget, x=200, y=35*2)
    treeview_base.add_widget(test_image, x=280, y=35*2)
    treeview_base.set_size_request(1500, 1500)
    scroll_win = gtk.ScrolledWindow()
    #
    node1 = treeview_base.nodes.add("root1")
    node2 = treeview_base.nodes.add("root2")
    node3 = treeview_base.nodes.add("root3")
    node4 = treeview_base.nodes.add("root4")
    node1_1 = node1.nodes.add("roo1-1")
    node1_2 = node1.nodes.add("roo1-2")
    node1_3 = node1.nodes.add("roo1-3")
    node1_1_1 = node1_1.nodes.add("root1-1-1")
    #
    scroll_win.add_with_viewport(treeview_base)
    win.add(scroll_win)
    win.show_all()
    gtk.main()



