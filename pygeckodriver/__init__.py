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

    arch = '64' if platform.machine().endswith('64') else '32'

    sys = platform.system()
    if sys == 'Darwin':
        path += 'macos'
    elif sys == 'Windows':
        path += 'win{}.exe'.format(arch)
    elif sys == 'Linux':
        path += 'linux{}'.format(arch)
    else:
        raise Exception('OS {} not supported'.format(sys))

    if not os.path.exists(path):
        raise FileNotFoundError('GeckoDriver for {}({}) '
                                'is not found.'.format(sys, arch))
    return path


geckodriver_path = _get_filename()
