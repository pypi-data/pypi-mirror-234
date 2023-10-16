#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
Copyright: Copyright 2019, unipark.io
'''
import os
import platform

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _get_executable():
    path = None

    sys = platform.system()
    arch = platform.machine().lower()
    if sys == 'Windows':
        if arch == 'amd64':
            path = os.path.join(_BASE_DIR, \
                    'chromedriver-win64', 'chromedriver.exe')
        else:
            path = os.path.join(_BASE_DIR, \
                    'chromedriver-win32', 'chromedriver.exe')
    else:
        if sys == 'Darwin':
            if arch.startswith('arm'):
                path = os.path.join(_BASE_DIR, \
                        'chromedriver-mac-arm64', 'chromedriver')
            else:
                path = os.path.join(_BASE_DIR, \
                        'chromedriver-mac-x64', 'chromedriver')
        elif sys == 'Linux':
            path = os.path.join(_BASE_DIR, \
                    'chromedriver-linux64', 'chromedriver')
        else:
            raise Exception('OS not supported')

        if not os.path.exists(path):
            raise FileNotFoundError('ChromeDriver for {}({}) '
                    'is not found.'.format(sys, arch))
    return path

chromedriver_path = _get_executable()
