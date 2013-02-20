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
import dbus
import dbus.service
import dbus.mainloop.glib

'''
as : 列表
s  : 字符串
(ss) : 元组
a{ss} : 字典
'''

DEEPIN_MEDIA_PLAYER_DBUS_NAME = "com.deepin_media_player.SampleInterface"

class DemoException(dbus.DBusException):
    _dbus_error_name = 'com.deepin_media_player.DemoException'

class SomeObject(dbus.service.Object):
    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='s', out_signature='')
    def play(self, path):
        print "play media player file...", path

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def next(self):
        print "next..next..next"

    @dbus.service.method(DEEPIN_MEDIA_PLAYER_DBUS_NAME,
                         in_signature='', out_signature='')
    def prev(self):
        print "prev...prev...prev"


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("com.deepin_media_player.SampleService", session_bus)
    object = SomeObject(session_bus, '/deepin_media_player')

    #mainloop = gobject.MainLoop()
    #mainloop.run()
    import gtk
    gtk.main()
