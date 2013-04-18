#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from widget.utils import is_file_audio, get_file_type


if __name__ == "__main__":
    path = "/media/文档/娱乐/音乐无极限"
    path = "/media/文档/娱乐/电影"
    '''
    print is_file_audio(os.path.join(path, "43D2FF79B8C65E7D.wma"))
    print is_file_audio(os.path.join(path, "BCA95FD95A16D3D9.zip"))
    print get_file_type(os.path.join(path, "BCA95FD95A16D3D9.zip"))
    '''
    print get_file_type(os.path.join(path, "王的盛宴TC[www.il168.com].rmvb"))
    print get_file_type(os.path.join(path, "喜羊羊与灰太狼过蛇年_2013_DVDscr.mp4"))

