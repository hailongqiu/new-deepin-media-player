#! /usr/bin/python
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


import os
import sys
import imp



class PluginManager(object):
    user_path = "/home/long/.config/deepin-media-player/plugins"
    def __init__(self, this=None, load_plugins_check=True, devel_plugin=None):
        self.__priority_order = ["ldmp", "global", "user"]
        self.plugin_dirs = {
                "ldmp":self.user_path,
                "global":self.user_path,
                "user":self.user_path
                }
        #
        self.__this              = this
        self.__devel_plugin_file = devel_plugin # 开发插件路径.
        self.__devel_plugin_name = None
        #
        self.__active_plugins             = {}
        self.__inactive_plugins           = {}
        self.__on_demand_active_plugins   = {}
        self.__on_demand_inactive_plugins = {}
        #
        self.__active_modules             = {}
        self.__inactive_modules           = {}
        self.__on_demand_active_modules   = {}
        self.__on_demand_inactive_modules = {}
        #
        self.__faile_modules              = {}

        self.__found_core_modules   = []
        self.__found_global_modules = []
        self.__found_user_modules   = []
        #
        self.__modules_count = 0
        pdirs_exist, msg = self.__plugin_directories_exist()
        if not pdirs_exist:
            raise PluginPathError(msg)
        #
        if load_plugins_check:
            if not self.__plugin_modules_exist():
                raise PluginModulesError
            self.__insert_plugin_paths()
            self.__load_plugins()
        #
        # self.__checkplugindownloaddirectory

    def finalize_setup(self):
        for module in self.__on_demand_active_modules.values() + \
                      self.__on_demand_inactive_modules.values():
            if hasattr(module, "module_setup"):
                module.module_setup()

    def get_plugindir(self, key):
        if key not in ["global", "user"]:
            return None
        else:
            try:
                return self.plugin_dirs[key]
            except KeyError:
                return None

    def __plugin_directories_exist(self):
        if self.__devel_plugin_file:
            path = os.path.split(self.__devel_plugin_file)[0]
            fname = os.path.join(path, "__init__.py")
            if not os.path.exists(fname):
                try:
                    f = open(fname, "wb")
                    f.close()
                except IOError:
                    return (False, "找不到文件" + self.__devel_plugin_file)
        if True:
            fname = os.path.join(self.plugin_dirs["user"], "__init__.py")
            if not os.path.exists(fname):
                # 如果用户插件目录不存在，则创建.
                if not os.path.exists(self.plugin_dirs["user"]):
                    os.mkdir(self.plugin_dirs["user"], 0755)
                try:
                    f = open(fname, "wb")
                    f.close()
                except IOError:
                    del self.plugin_dirs["user"]

            #if not os.path.exists(self.plugin_dirs["global"]) and \
            #   os.access( # 判断全局插件目录是否可写入.
            # 再判断是否存在.
        else:
            del self.plugin_dirs["user"]
            del self.plugin_dirs["global"]

        if not os.path.exists(self.plugin_dirs["ldmp"]):
            return (False, "找不到" + self.plugin_dirs["ldmp"])

        return (True, "")


    def __plugin_modules_exist(self):
        # 目录下自带的插件.
        self.__found_core_modules = self.get_plugin_modules(self.plugin_dirs["ldmp"])
        # 全局文件夹下的插件.
        if self.plugin_dirs.has_key("global"):
            self.__found_global_modules = self.get_plugin_modules(self.plugin_dirs["global"])
        # 配置文件夹下的插件.
        if self.plugin_dirs.has_key("user"):
            self.__found_user_modules = self.get_plugin_modules(self.plugin_dirs["user"])

        return len(self.__found_core_modules +
                   self.__found_global_modules + 
                   self.__found_user_modules) > 0

    def get_plugin_modules(self, plugin_path):
        # 过滤不是插件的文件.
        print "get_plugin_modules:", plugin_path
        files = [f[:-3] for f in os.listdir(plugin_path) \
                 if self.is_valid_plugin_name(f)]
        plugin_files = files
        return plugin_files[:]

    def is_valid_plugin_name(self, plugin_name):
        # 判断是否为插件正规的格式并且为.py后缀的文件.
        return (plugin_name.startswith("plugin_") and
                plugin_name.endswith(".py"))

    def __insert_plugin_paths(self):
        for key in self.__priority_order:
            if self.plugin_dirs.has_key(key):
                if not self.plugin_dirs[key] in sys.path:
                    # 将系统搜索路径加入到sys.path.
                    sys.path.insert(2, self.plugin_dirs[key])
                # UI.PixmapCache.AddSearchPath...
        # self.__develPluginFile:...

    def __load_plugins(self):
        # 加载插件.
        ##############################################
        # 加载开发目录插件测试.
        devel_plugin_name = ""
        if self.__devel_plugin_file:
            devel_plugin_path, devel_plugin_name = \
                    os.path.split(self.__devel_plugin_name)
            if self.is_valid_plugin_name(devel_plugin_name):
                devel_plugin_name = devel_plugin_name[:-3]
        
        ##############################################
        # 加载自带插件.
        for plugin_name in self.__found_core_modules:
            if plugin_name not in self.__found_global_modules and \
               plugin_name not in self.__found_user_modules and \
               plugin_name != devel_plugin_name:
               self.load_plugin(plugin_name, self.plugin_dirs["ldmp"])
        ##############################################
        # 加载全局插件.
        for plugin_name in self.__found_global_modules:
            if plugin_name not in self.__found_user_modules and \
               plugin_name != devel_plugin_name:
               self.load_plugin(plugin_name, self.plugin_dirs["global"])
        ###############################################
        # 加载用户目录插件.
        for plugin_name in self.__found_user_modules:
            if plugin_name != devel_plugin_name:
                self.load_plugin(plugin_name, self.plugin_dirs["user"])
        ###############################################
        if devel_plugin_name:
            self.load_plugin(devel_plugin_name, devel_plugin_path)
            self.__devel_plugin_name = devel_plugin_name

    def load_plugin(self, name, directory, reload_ = False):
        # 加载插件.
        try:
            fname = "%s.py" % os.path.join(directory, name)
            module = imp.load_source(name, fname)
            #判断是否有这个函数.
            if not hasattr(module, "autoactivate"):
                module.error = "error loadingatrrr...."
                # 失败的模块.
                self.__faile_modules[name] = module
                raise PluginLoadError(name)
            if getattr(module, "autoactivate"): # 如果模块中有auto...
                self.__inactive_plugins[name] = module
            else:
                if not hasattr(module, "plugin_type") or \
                   not hasattr(module, "plugin_typename"):
                    module.error = "模块没有 plugin_type 或者 plugin_typename函数"
                    self.__faile_modules[name] = module
                    raise PluginLoadError(name)
                else:
                    self.__on_demand_inactive_modules[name] = module

            module.module_name = name
            module.module_file_name = fname
            self.__modules_count += 1
            #
            if reload_: # 判断是否加载.热更新.
                reload(module)
        except PluginLoadError:
            print "Error loading plugin module:", name
        except StandardError, err:
            module = imp.new_module(name)
            module.error = \
                    "模块加载失败" + name + str(err)
            print "load plugin==>>error:", err
            print unicode(err)

    def unload_plugin(self, name, directory):
        fname = "%s.py" % os.path.join(directory, name)
        #
        if (self.__on_demand_active_modules.has_key(name) and
            self.__on_demand_active_modules[name].module_file_name == fname):
            return False

        if (self.__active_modules.has_key(name) and 
            self.__active_modules[name].module_file_name == fname): 
            try:
                del self.__inactive_plugins[name]
            except KeyError:
                pass
            del self.__inactive_modules[name]
        elif (self.__on_demand_inactive_modules.has_key(name) and 
              self.__on_demand_inactive_modules[name].module_file_name == fname):
            try:
                del self.__on_demand_inactive_plugins[name]
            except KeyError:
                pass
        elif self.__faile_modules.has_key(name):
            del self.__faile_modules[name]

        self.__modules_count -= 1 # 模块卸载计数.
        return True

    def remove_plugin_from_sys_modules(self, plugin_name, package, internal_packages):
        packages = [package] + internal_packages
        found = False
        if not package:
            package = "__None__"

        for module_name in sys.modules.keys()[:]:
            if (module_name == plugin_name or 
                module_name.split(".")[0] in packages):
                found = True
                del sys.modules[module_name]
        return found

    def init_on_demand_plugins(self):
        names = sorted(self.__on_demand_inactive_modules.keys())
        for name in names:
            self.init_on_demand_plugin(name)

    def init_on_demand_plugins(self, name):
        try:
            try:
                module = self.__on_demand_inactive_modules[name]
            except KeyError:
                return None

            if not self.__can_activate_plugin(module):
                raise PluginActivationError(module.module_name)
            version = getattr(module, "version")
            class_name = getattr(module, "class_name")
            plugin_class = getattr(module, class_name)
            plugin_object = None
            if not slef.__on_demand_inactive_plugins.has_key(name):
                plugin_object = plugin_class(self.this)
                plugin_object.module = module
                plugin_object.name = class_name
                plugin_object.version = version
                # 插件成功.
                self.__on_demand_inactive_plugins[name] = plugin_object
        except PluginActivationError:
            return None

class PluginError(Exception):
    def __init__(self):
        self._error_message

    def __repr__(self):
        return unicode(self._error_message)

    def __str__(self):
        return str(self._error_message)

class PluginLoadError(PluginError):
    def __init__(self, msg=None):
        self._error_message = "pluginloaderror[error]:" + msg

class PluginModulesError(PluginError):
    def __init__(self, name):
        self._error_message = "PluginModulesError[error]:" + msg

class PluginPathError(PluginError):
    def __init__(self, msg=None):
        if msg:
            self._error_message = msg
        else:
            self._error_message = "PluginPathError[error]:" + "找不到"

class PluginActivationError(PluginError):
    def __init__(self, msg=None):
        self._error_message = "PluginActivationError[error]:", msg


    
if __name__ == "__main__":
    plugin_man = PluginManager()
