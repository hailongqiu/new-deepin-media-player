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
from draw  import draw_text, draw_pixbuf
from utils import get_text_size
import gtk
from gtk import gdk
import gobject
import random


def type_check(type_name, type_str):
    return type(type_name).__name__ == type_str

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
        #
        self.children = []
        #
        self.__nodes_list = []
        self.nodes = Nodes()
        self.nodes.connect("update-data", self.__nodes_update_data_event)
        self.nodes.connect("added-data",  self.__nodes_added_data_event)
        self.nodes.connect("remove-data", self.__nodes_remove_data_event)
        self.__init_values_columns()

    def __nodes_update_data_event(self, node):
        # 当有数据更新时,进行重绘.
        print "__nodes_update_data_event... nodes;", node.text

    def __nodes_added_data_event(self, node):
        # 添加数据更新树型结构的映射列表.
        if node.parent == self.nodes:
            self.__nodes_list.append(node.nodes)
        else:
            parent = node.parent
            node_to_parent_index = parent.index(node)
            parent_to_list_index = self.__nodes_list.index(parent)
            self.__nodes_list.insert(parent_to_list_index + node_to_parent_index,
                                     node.nodes)
        

    def __nodes_remove_data_event(self, node):
        # 当有数据删除时,更新映射列表.
        print "__nodes_remove_data_event...: 删除-->", node.text

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
            pass
        #
        return False

    def do_motion_notify_event(self, e):
        #print "do--mo--no--ev", e.x
        if e.window == self.window:
            self.index = int(e.y) / self.node_height
            self.queue_draw()
        return False

    def do_button_press_event(self, e):
        print "do_button_press_event..."
        self.__save_y = 0
        self.__save_node = None
        self.__end_node  = None
        node = self.__get_tree_view_nodes_data(e, self.nodes)
        if node:
            print "找到了:", node.text, node.leave
        #print "node:", node.text

        return False

    def __get_tree_view_nodes_data(self, e, nodes):
        index = int(e.y / self.node_height)
        for node in nodes:
            print node
            if int(self.__save_y / self.node_height) == index:
                #print "node.text:", node.text
                #self.__save_node = node
                return node
            if node.is_expanded:
                if node.nodes:
                    self.__save_y += self.node_height
                    node = self.__get_tree_view_nodes_data(e, node.nodes)
                    if node:
                        return node
                else:
                    self.__save_y += self.node_height
            else:
                self.__save_y += self.node_height

    def do_button_release_event(self, e):
        print "do_button_release_event..."
        return False

    def do_enter_notify_event(self, e):
        #print "do_enter_notify_event..."
        return False

    def do_leave_notify_event(self, e):
        #print "do_leave_notify_event..."
        return False

    def do_key_press_event(self, e):
        print "do_key_press_event..."

    def do_key_release_event(self, e):
        print "do_key_release_event..."

    def do_size_request(self, req):
        '''
        for child in self.children:
            child.widget.size_request()
        '''

    def do_size_allocate(self, allocation):
        print "do_size_allocate..."
        gtk.Container.do_size_allocate(self, allocation)
        '''
        for child in self.children:
            allocation = gdk.Rectangle()
            allocation.x  = child.x
            allocation.y  = child.y
            allocation.width = child.w 
            allocation.height = child.h 
            child.widget.size_allocate(allocation)
        '''
        #
        if self.get_realized():
            self.window.move_resize(
                    self.allocation.x,
                    self.allocation.y,
                    self.allocation.width,
                    self.allocation.height)

    def do_show(self):
        gtk.Container.do_show(self)
        #self.edit_entry.set_visible(False)

    def do_destroy(self):
        print "do_destroy..."

    def do_forall(self, include_internals, callback, data):
        '''
        for child in self.children:
            callback(child.widget, data)
        '''
        pass

    def add_widget(self, child, x=0, y=0, w=0, h=0):
        if self.window:
            child.set_parent_window(self.window)
        else:
            child.set_parent(self)
        tree_view_child = TreeViewChild()
        tree_view_child.widget = child
        tree_view_child.x = x
        tree_view_child.y = y
        tree_view_child.w = max(w, 80)
        tree_view_child.h = max(h, self.node_height)
        self.children.append(tree_view_child)

gobject.type_register(TreeViewBase)


class NodesEvent(object):
    def __init__(self):
        self.cr = None
        self.x  = 0
        self.y  = 0
        self.w  = 0
        self.h  = 0
        self.node = None


class Nodes(list):
    def __init__(self):
        list.__init__(self)
        self.this = None
        self.__function_dict = {}

    def add(self, text):
        node = Node()
        node.text = text
        node.parent = self
        if self.this:
            node.leave  = self.this.leave + 1
        node.connect("update-data", self.__node_update_data_event)
        node.connect("added-data",  self.__node_added_data_event)
        node.connect("remove-data", self.__node_remove_data_event)
        self.append(node)
        self.emit("added-data", node)
        return node

    def delete(self, node):
        self.remove(node)
        self.emit("remove-data", node)
        for child_node in node.nodes:
            node.nodes.delete(child_node)

    def __node_update_data_event(self, node):
        self.emit("update-data", node)

    def __node_added_data_event(self, node):
        self.emit("added-data", node)

    def __node_remove_data_event(self, node):
        self.emit("remove-data", node)

    def connect(self, event_name, function_point):
        self.__function_dict[event_name] = function_point

    def emit(self, event_name, *arg):
        if self.__function_dict.has_key(event_name):
            self.__function_dict[event_name](*arg)

class Node(object):
    def __init__(self):
        self.__function_dict = {}
        self.text  = ""
        #self.sub_items = SubItems()
        self.__pixbuf      = None
        self.children = []
        #
        self.nodes = Nodes()
        self.nodes.this = self
        self.nodes.connect("update-data", self.__nodes_update_data_event)
        self.nodes.connect("added-data",  self.__nodes_added_data_event)
        self.nodes.connect("remove-data", self.__nodes_remove_data_event)
        #
        self.parent = None # 获取当前树节点的夫节点.
        self.leave  = 0    # 树的深度,不懂的看数据结构.
        self.__last_node  = []   # 获取最后一个子树节点.
        self.__first_node = []   # 获取树节点集合中的第一个子树节点.
        self.__next_node  = []   # 获取下一个同级节点.
        self.__prev_node  = []   # 获取上一个同级节点.
        self.__index      = None # 获取树节点在树节点集合中的位置.
        ####################
        self.is_expanded = True # 是否展开状态.
        self.is_selected = False # 是否选中状态.
        self.is_editing  = False # 是否可编辑状态.
        ####################
        self.node_font   = None  # 字体.
        self.next_visible_node = None # 获取下一个可见树节点.
        self.is_visible  = True # 是否可见.

    def __nodes_update_data_event(self, nodes):
        self.emit("update-data", nodes)

    def __nodes_added_data_event(self, nodes):
        self.emit("added-data", nodes)

    def __nodes_remove_data_event(self, nodes):
        self.emit("remove-data", nodes)

    def connect(self, event_name, function_point):
        self.__function_dict[event_name] = function_point

    def emit(self, event_name, *arg):
        if self.__function_dict.has_key(event_name):
            self.__function_dict[event_name](*arg)

    '''
    def add_widget(self, child_widget):
        self.children.append(child_widget)
    '''

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.emit("update-data", self)

    @text.getter
    def text(self):
        return self.__text

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

    @property
    def pixbuf(self):
        return self.__pixbuf

    @pixbuf.getter
    def pixbuf(self):
        return self.__pixbuf

    @pixbuf.setter
    def pixbuf(self, pixbuf):
        self.__pixbuf = pixbuf
        #self.emit()

    @pixbuf.deleter
    def pixbuf(self, pixbuf):
        del self.__pixbuf


if __name__ == "__main__":
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(300, 300)
    treeview_base = TreeViewBase()
    treeview_base.set_size_request(1500, 15000)
    scroll_win = gtk.ScrolledWindow()
    #
    node1 = treeview_base.nodes.add("root1")
    node2 = treeview_base.nodes.add("root2")
    node3 = treeview_base.nodes.add("root3")
    node4 = treeview_base.nodes.add("root4")
    '''
    for i in range(1, 30000):
        treeview_base.nodes.add("root" + str(i))
    '''
    node1_1 = node1.nodes.add("roo1-1")
    node1_2 = node1.nodes.add("roo1-2")
    node1_3 = node1.nodes.add("roo1-3")
    node1_1_1 = node1_1.nodes.add("root1-1-1")
    node1_1_2 = node1_1.nodes.add("root1-1-2")
    node1_2_1 = node1_2.nodes.add("root1-2-1")
    node1_4 = node1.nodes.add("roo1-4")
    node1_5 = node1.nodes.add("roo1-5")
    print node1.nodes[1].next_node.text
    print node1.nodes[1].prev_node.text
    node1.nodes[1].text = "fjdskf"
    treeview_base.nodes.delete(node1)
    #
    #
    scroll_win.add_with_viewport(treeview_base)
    win.add(scroll_win)
    win.show_all()
    gtk.main()



