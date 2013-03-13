
class plugin_class_name(object):
    def __init__(self):
        pass
     		  
    def init_values(self, this, gui, ldmp): # 初始化传过来的变量.
        pass
    
    def auto(self): # 是否自动运行插件. True 自动 False 不自动
        return True
		  
    def start(self): # 开启插件.
        print "start plugin..."
		  
    def stop(self): # 关闭插件.
        print "stop plugin..."
		  
    def name(self): # 插件唯一名字[主要用于其它插件控制我们的插件和调用我们插件的API].
        return "deepin_media_player_plugin_class_name_***" 
		  
    def insert(self): # 插入插件运行队列 
        return None
		  
    def icon(self): # 插件图标.
        return None
		  
    def version(self): # 插件版本.
        return "2.0"
    
    def author(self): # 开发者.
        return "hailongqiu"
	  
	  
def return_plugin(): 
    return plugin_class_name # 需要返回的类名.

