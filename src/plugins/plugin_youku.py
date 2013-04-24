#!coding:utf-8 
import gtk


class_name = "Test"
version = "1.0"
auto_check = True

class Test(object):
    def __init__(self, this):
        self.this = this
        self.btn = gtk.Button("插件youku")
        
    def start_plugin(self):
        self.this.vbox.pack_start(self.btn)
        self.this.vbox.show_all()
        print "start_plugin."
        return None, True
        
    def stop_plugin(self):
        print "end_plugin..."
        self.this.vbox.remove(self.btn)
        
