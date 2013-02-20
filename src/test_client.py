
import dbus
import sys


if __name__ == "__main__":
    bus = dbus.SessionBus()

    try:
        remote_object = bus.get_object("com.deepin_media_player.SampleService",
                                       "/deepin_media_player")
    except dbus.DbusException:
        sys.exit(1)
            
    iface = dbus.Interface(remote_object,
                           "com.deepin_media_player.SampleInterface")
    print iface.play("i love c and linux /test/debus.com")
    iface.next()
    iface.prev()
