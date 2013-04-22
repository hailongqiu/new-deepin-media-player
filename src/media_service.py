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

import gobject
import gtk
import dbus
import dbus.service
import dbus.mainloop.glib
from locales import _ # 国际化翻译.

'''
as    : 列表
s     : 字符串
(ss)  : 元组
a{ss} : 字典
'''

#DEEPIN_MEDIA_PLAYER_DBUS_NAME = "com.deepin_media_player.SampleInterface"

DEEPIN_MEDIA_DBUS_NAME_PROPERTY = "org.freedesktop.DBus.Properties"
DEEPIN_MEDIA_DBUS_NAME = "org.mpris.MediaPlayer2"
DEEPIN_MEDIA_PLAYER_DBUS_NAME = "org.mpris.MediaPlayer2.Player"


class DemoException(dbus.DBusException):
    _dbus_error_name = 'com.deepin_media_player.DemoException'

class SomeObject(dbus.service.Object):
    properties = {'Identity': _('深度影音'), 'DesktopEntry': 'deepin-media-player'}
    player_properties = {'PlaybackStatus': 'Stopped', 'Volume': 1.0, 'Metadata': {'xesam:title': ""}}
    def set_dmp(self, app):
        self.this  = app
        self.ldmp = self.this.ldmp
        self.ldmp.connect("start-media-player", self.dbus_ldmp_start_media_player)
        self.ldmp.connect("end-media-player",   self.dbus_ldmp_end_media_player)

    def dbus_ldmp_start_media_player(self, ldmp):    
        from widget.utils import get_play_file_name
        file_name = get_play_file_name(ldmp.player.uri)
        self.player_properties["PlaybackStatus"] = "Playing"
        data = {
                "mpris:trackid":'o',
                "xesam:title":file_name,
                }
        self.player_properties["Metadata"] = data

    def dbus_ldmp_end_media_player(self, ldmp):
        print "停止播放..."
        self.player_properties["PlaybackStatus"] = "Stopped"
        self.player_properties["Metadata"]["xesam:title"] = ""

    '''play video/audio file.'''
    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def Play(self):
        print "play media player file..."

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def Pause(self):
        print "pause.. pause..pause.."
        self.ldmp.pause()

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def Stop(self):  
        print "stop stop stop ..."
        self.ldmp.stop()

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def Next(self):  # next play file.
        print "next..next..next"
        self.this.next()

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def Previous(self): # prev play file.
        print "prev...prev...prev"
        self.this.prev()

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='i', out_signature='')
    def fseek(self, value): # prev play file.
        print "prev...prev...prev"
        self.ldmp.fseek(value)


    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='i', out_signature='')
    def bseek(self, value): # prev play file.
        print "prev...prev...prev"
        self.ldmp.bseek(value)

    @dbus.service.method(DEEPIN_MEDIA_DBUS_NAME,
                         in_signature='', out_signature='')
    def Quit(self): # prev play file.
        print "prev...prev...prev"
        self.ldmp.quit()
        gtk.main_quit()


    @dbus.service.method(DEEPIN_MEDIA_DBUS_NAME,
                         in_signature='', out_signature='')
    def Raise(self): # prev play file.
        pass

    @dbus.service.method(DEEPIN_MEDIA_DBUS_NAME_PROPERTY,
                         in_signature='ss', out_signature='v')
    def Get(self, interface, prop):
        if interface == "org.mpris.MediaPlayer2":
            if prop in self.properties:
                return self.properties[prop]
            return ""
        elif interface == "org.mpris.MediaPlayer2.Player":
            if prop in self.player_properties:
                return self.player_properties[prop]
            return ""

    @dbus.service.method(DEEPIN_MEDIA_DBUS_NAME_PROPERTY,
                         in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface):
        print "*********get all... getall", interface
        if interface == "org.mpris.MediaPlayer2":
            return self.properties
        elif interface == "org.mpris.MediaPlayer2.Player":
            return self.player_properties

    @dbus.service.method(DEEPIN_MEDIA_DBUS_NAME_PROPERTY,
                         in_signature='ssv', out_signature='')
    def Set(self, interface, prop, value):                                      
        print "Set", interface, prop, value
        if interface == "org.mpris.MediaPlayer2.Player":
            self.player_properties[prop] = value
            self.this.key_set_volume(int(value * 100))

                                                                            
    @dbus.service.signal(DEEPIN_MEDIA_DBUS_NAME_PROPERTY, signature='sa{sv}as')           
    def PropertiesChanged(self, interface, updated, invalid):                   
        pass                                                     

    @dbus.service.signal(DEEPIN_MEDIA_PLAYER_DBUS_NAME, signature='x')
    def Seeked(self, pos):
        pass 



