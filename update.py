#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
Copyright: Copyright 2019, unipark.io
'''
import os
import re
import requests
import json
import tarfile
import gzip
from decouple import config
from zipfile import ZipFile
from io import BytesIO

PACKAGE_NAME = 'pygeckodriver'
PACKAGE_URL = 'https://test.pypi.org/pypi/pygeckodriver/json' \
        if config('DEBUG', default=False, cast=bool) \
        else 'https://pypi.org/pypi/pygeckodriver/json'

GECKODRIVER_URL = 'https://api.github.com/repos/mozilla/geckodriver/releases'
OS_TYPES = [ 'win', 'mac', 'linux' ]
ARCHITECTURE = [ '32', '64' ]
FILE_NAME = 'geckodriver_'

DOWNLOAD_DIR = './pygeckodriver/'
VERSION_FILE = './VERSION.txt'

def compare_version(alpha, beta):
    alpha_arr = alpha.split('.')
    beta_arr = beta.split('.')

    while alpha_arr and beta_arr:
        m = int(alpha_arr.pop(0))
        n = int(beta_arr.pop(0))
        if m > n:
            return 1
        elif m < n:
            return -1

    while alpha_arr:
        m = int(alpha_arr.pop(0))
        if m > 0:
            return 1

    while beta_arr:
        n = int(beta_arr.pop(0))
        if n > 0:
            return -1
    return 0

def get_pip_version():
    page = requests.get(PACKAGE_URL)
    return json.loads(page.text)['info']['version']

def get_next_version(prev_version):
    version_lst = get_geckodriver_versions()
    while version_lst:
        next_version = version_lst.pop(0)['tag_name'].strip('v')
        if compare_version(prev_version, next_version) == -1:
            return next_version
    return None

def get_geckodriver_versions():
    cont = requests.get(GECKODRIVER_URL).text
    data = [ i for i in json.loads(cont) if 'geckodriver' in i['assets'][0]['name'] ]
    return list(reversed(data))

def download_geckodriver(version):
    cont = requests.get(GECKODRIVER_URL).text
    data = json.loads(cont)
    for v in data:
        if version == v['tag_name'].strip().strip('v'):
            for asset in v['assets']:
                url = asset['browser_download_url']
                print("Download file: ", url)
                platform = asset['name'].split('-').pop().split('.').pop(0)
                if platform.lower() in ('osx', 'macos'):
                    filename = 'geckodriver_macos'
                else:
                    filename = 'geckodriver_{}'.format(platform)

                if 'win32' in filename \
                        or 'win64' in filename:
                    filename += '.exe'

                if asset['name'].endswith('.tar.gz'):
                    tf = tarfile.open(fileobj=BytesIO(requests.get(url).content))
                    for f in tf.getnames():
                        if 'geckodriver' in f:
                            tf.extract(f, path=DOWNLOAD_DIR)
                            os.rename(os.path.join(DOWNLOAD_DIR, f), \
                                    os.path.join(DOWNLOAD_DIR, filename))
                            os.chmod(os.path.join(DOWNLOAD_DIR, filename), 0o755)
                elif asset['name'].endswith('.gz'):
                    gf = gzip.GzipFile(fileobj=BytesIO(requests.get(url).content))
                    with open(os.path.join(DOWNLOAD_DIR, filename), 'wb') as f:
                        f.write(gf.read())
                    os.chmod(os.path.join(DOWNLOAD_DIR, filename), 0o755)
                elif '.zip' in asset['name']:
                    zf = ZipFile(BytesIO(requests.get(url).content))
                    for f in zf.namelist():
                        if 'geckodriver' in f:
                            zf.extract(f, DOWNLOAD_DIR)
                            os.rename(os.path.join(DOWNLOAD_DIR, f), \
                                    os.path.join(DOWNLOAD_DIR, filename))
                            os.chmod(os.path.join(DOWNLOAD_DIR, filename), 0o755)
            break


if __name__ == '__main__':
    version = os.environ.get('VERSION')
    force_upload = False

    if version:
        force_upload = True

    if not force_upload:
        pip_version = get_pip_version()
        print('Current PyPI version:', pip_version)

        version = get_next_version(pip_version)
        print('Version to update:', version)
        if not version:
            print('Latest version.')
            exit(1)

        download_geckodriver(version)
        with open(VERSION_FILE, 'w') as f:
            f.write(version)
    else:
        download_geckodriver(version)
        with open(VERSION_FILE, 'w') as f:
            f.write(version)
