#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
Copyright: Copyright 2019, unipark.io
'''
import os
import platform

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _get_filename():
    path = os.path.join(_BASE_DIR, 'geckodriver_')

    sys = platform.system()
    arch = platform.machine()
    file_extension = None
    if sys == 'Darwin':
        path += 'macos'
    else:
        if sys == 'Windows':
            path += 'win'
            file_extension = ".exe"
        elif sys == 'Linux':
            path += 'linux'
        else:
            raise Exception('OS not supported')
        path += '64' if arch.endswith('64') else '32'
        path += file_extension

    if not os.path.exists(path):
        raise FileNotFoundError('GeckoDriver for {}({}) '
                                'is not found.'.format(sys, arch))
    return path


geckodriver_path = _get_filename()
