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

'''
as    : 列表
s     : 字符串
(ss)  : 元组
a{ss} : 字典
'''

DEEPIN_MEDIA_PLAYER_DBUS_NAME = "com.deepin_media_player.SampleInterface"

class DemoException(dbus.DBusException):
    _dbus_error_name = 'com.deepin_media_player.DemoException'

class SomeObject(dbus.service.Object):
    def set_dmp(self, app):
        self.app  = app
        self.ldmp = app.ldmp

    '''play video/audio file.'''
    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def play(self):
        print "play media player file..."
        self.ldmp.play()

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def pause(self):
        print "pause.. pause..pause.."
        self.ldmp.pause()

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def stop(self):  
        print "stop stop stop ..."
        self.ldmp.stop()

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def next(self):  # next play file.
        print "next..next..next"
        self.app.next()

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def prev(self): # prev play file.
        print "prev...prev...prev"
        self.app.prev()

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

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def quit(self): # prev play file.
        print "prev...prev...prev"
        self.ldmp.quit()
        gtk.main_quit()

