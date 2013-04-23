#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
from widget.utils import is_file_audio, get_file_type
from format_conv.gui import Form


if __name__ == "__main__":
    win = Form()
    win.show_all()

    gtk.main()
