#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
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



from dtk.ui.new_treeview import TreeView, TreeItem
from dtk.ui.draw import draw_text
import gobject
import gtk

class plugin_class_name(object):
    def __init__(self):
        items = [PlayListItem("歌曲", "我得房间"),
                 PlayListItem("歌曲", "我得房间"),
                 PlayListItem("歌曲", "我得房间"),
                 PlayListItem("歌曲", "我得房间"),
                 PlayListItem("歌曲", "我得房间"),
                 PlayListItem("歌曲", "我得房间"),
                 PlayListItem("歌曲", "我得房间"),
                 PlayListItem("歌曲", "我得房间"),
                 PlayListItem("歌曲", "我得房间"),
                 PlayListItem("歌曲", "我得房间")]
        self.play_list_view = TreeView(items)
        self.play_list_view.set_size_request(120, 80)
        # init play_list_view events.
        # treeview.connect("delete-select-items", m_delete_select_items)
        # treeview.connect("button-press-item", m_button_press_item)
        # treeview.connect("double-click-item", m_double_click_item)
        # treeview.connect("right-press-items", m_right_press_items)
        # treeview.connect("single-click-item", m_single_click_item)    
        
    def init_values(self, this, gui, ldmp):		  
        self.this = this
        self.gui = gui
        self.ldmp = ldmp
        
    def auto(self): 
        return True
		  
    def start(self):
        self.gui.screen_and_play_list_hbox.pack_start(self.play_list_view, False, False)
        self.gui.screen_and_play_list_hbox.show_all()
        
    def stop(self): 
        self.gui.screen_and_play_list_hbox.remove(self.play_list_view)
		  
    def name(self): 
        return "deepin_media_player_play_list_tree_view" 
		  
    def insert(self): 
        return None
		  
    def icon(self): 
        return None
		  
    def version(self):
        return "2.0"
    
    def author(self):
        return "hailongqiu"
	  
	  
def return_plugin(): 
    return plugin_class_name



class PlayListItem(TreeItem):
    __gsignals__ = {"select": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (int,))}
    '''a shortcut item in TreeView'''
    def __init__(self, description, keyname): 
        TreeItem.__init__(self)
        self.description = description
        self.keyname = keyname
        self.height = 24
        self.padding_x = 5
        self.COLUMN_ACCEL = 1
    
    def get_height(self):
        return self.height
    
    def get_column_widths(self):
        return [150, 270]
    
    def get_column_renders(self):
        return [self.render_description, self.render_keyname]
        
    def render_description(self, cr, rect):
        if self.is_select:
            text_color = "#FFFFFF"
            bg_color = "#3399FF"
            cr.set_source_rgb(*color_hex_to_cairo(bg_color))
            cr.rectangle(rect.x, rect.y, rect.width, rect.height)
            cr.paint()
        else:
            text_color = "#000000"
        draw_text(cr, self.description, rect.x+self.padding_x, rect.y, rect.width, rect.height, text_color=text_color)
    
    def render_keyname(self, cr, rect):
        if self.is_select:
            text_color = "#FFFFFF"
            bg_color = "#3399FF"
            cr.set_source_rgb(*color_hex_to_cairo(bg_color))
            cr.rectangle(rect.x, rect.y, rect.width, rect.height)
            cr.paint()
        else:
            text_color = "#000000"
        draw_text(cr, self.keyname, rect.x+self.padding_x, rect.y, rect.width, rect.height, text_color=text_color)
    
gobject.type_register(PlayListItem)
