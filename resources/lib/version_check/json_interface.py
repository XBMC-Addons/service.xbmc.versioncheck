# -*- coding: utf-8 -*-

"""

    Copyright (C) 2013-2014 Team-XBMC
    Copyright (C) 2014-2019 Team Kodi

    This file is part of service.xbmc.versioncheck

    SPDX-License-Identifier: GPL-3.0-or-later
    See LICENSES/GPL-3.0-or-later.txt for more information.

"""

import json as json_interface
import os
import sys

import xbmc
import xbmcvfs

from .common import ADDON_PATH


def get_installed_version():
    # retrieve current installed version
    query = {
        "jsonrpc": "2.0",
        "method": "Application.GetProperties",
        "params": {
            "properties": ["version", "name"]
        },
        "id": 1
    }
    json_query = xbmc.executeJSONRPC(json_interface.dumps(query))
    if sys.version_info[0] >= 3:
        json_query = str(json_query)
    else:
        json_query = unicode(json_query, 'utf-8', errors='ignore')
    json_query = json_interface.loads(json_query)
    version_installed = []
    if 'result' in json_query and 'version' in json_query['result']:
        version_installed = json_query['result']['version']
    return version_installed


def get_version_file_list():
    # retrieve version lists from supplied version file
    version_file = os.path.join(ADDON_PATH, 'resources/versions.txt')
    file = xbmcvfs.File(version_file)
    data = file.read()
    file.close()
    if sys.version_info[0] >= 3:
        version_query = str(data)
    else:
        version_query = unicode(data, 'utf-8', errors='ignore')
    version_query = json_interface.loads(version_query)
    return version_query
