#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

    Copyright (C) 2011-2013 Martijn Kaijser
    Copyright (C) 2013-2014 Team-XBMC
    Copyright (C) 2014-2019 Team Kodi

    This file is part of service.xbmc.versioncheck

    SPDX-License-Identifier: GPL-3.0-or-later
    See LICENSES/GPL-3.0-or-later.txt for more information.

"""

import os
import sys

import xbmc  # pylint: disable=import-error
import xbmcaddon  # pylint: disable=import-error
import xbmcgui  # pylint: disable=import-error

_ADDON = xbmcaddon.Addon('service.xbmc.versioncheck')
_ADDON_NAME = _ADDON.getAddonInfo('name')
if sys.version_info[0] >= 3:
    _ADDON_PATH = _ADDON.getAddonInfo('path')
else:
    _ADDON_PATH = _ADDON.getAddonInfo('path').decode('utf-8')
_ICON = _ADDON.getAddonInfo('icon')


class Viewer:
    """ Viewer class
    """
    # constants
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__(self, *args, **kwargs):
        _ = args
        _ = kwargs
        # activate the text viewer window
        xbmc.executebuiltin('ActivateWindow(%d)' % (self.WINDOW,))
        # get window
        self.window = xbmcgui.Window(self.WINDOW)
        # give window time to initialize
        xbmc.sleep(100)
        # set controls
        self.set_controls()

    def set_controls(self):
        """ Set the window controls
        """
        # get header, text
        heading, text = self.get_text()
        # set heading
        self.window.getControl(self.CONTROL_LABEL).setLabel('%s : %s' % (_ADDON_NAME, heading,))
        # set text
        self.window.getControl(self.CONTROL_TEXTBOX).setText(text)
        xbmc.sleep(2000)

    def get_text(self):
        """ Get heading and text

        :return: gotham-alpha_notice or empty strings
        :rtype: str, str
        """
        try:
            if sys.argv[1] == 'gotham-alpha_notice':
                return 'Call to Gotham alpha users', \
                       self.read_file(os.path.join(_ADDON_PATH,
                                                   'resources/gotham-alpha_notice.txt'))
        except Exception as error:  # pylint: disable=broad-except
            xbmc.log(_ADDON_NAME + ': ' + str(error), xbmc.LOGERROR)
        return '', ''

    @staticmethod
    def read_file(filename):
        """ Read the contents of the provided file

        :param filename: path and name of file to read
        :type filename: str
        :return: contents of the provided file
        :rtype: str
        """
        with open(filename) as open_file:
            contents = open_file.read()
        return contents


class WebBrowser:
    """ Display url using the default browser
    """

    def __init__(self, *args, **kwargs):
        _ = args
        _ = kwargs
        try:
            url = self.get_url()
            # notify user
            self.notification(_ADDON_NAME, url)
            xbmc.sleep(100)
            # launch url
            self.launch_url(url)
        except Exception as error:  # pylint: disable=broad-except
            xbmc.log(_ADDON_NAME + ': ' + str(error), xbmc.LOGERROR)

    @staticmethod
    def notification(heading, message, icon=None, time=15000, sound=True):
        """ Create a notification

        :param heading: notification heading
        :type heading: str
        :param message: notification message
        :type message: str
        :param icon: path and filename for the notification icon
        :type icon: str
        :param time: time to display notification
        :type time: int
        :param sound: is notification audible
        :type sound: bool
        """
        if not icon:
            icon = _ICON
        xbmcgui.Dialog().notification(heading, message, icon, time, sound)

    @staticmethod
    def get_url():
        """ Get the url

        :return: url - sys.argv[2]
        :rtype: str
        """
        return sys.argv[2]

    @staticmethod
    def launch_url(url):
        """ Open url in a web browser

        :param url: url to open
        :type url: str
        """
        import webbrowser  # pylint: disable=import-outside-toplevel
        webbrowser.open(url)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'webbrowser':
            WebBrowser()
        else:
            Viewer()
    except Exception as err:  # pylint: disable=broad-except
        xbmc.log(_ADDON_NAME + ': ' + str(err), xbmc.LOGERROR)
