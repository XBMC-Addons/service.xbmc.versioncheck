#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2013 Team-XBMC
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import xbmc
import xbmcgui
import lib.common
from lib.common import log, dialog_yesno, message_info, set_password
from lib.common import upgrade_message as _upgrademessage
from lib.common import upgrade_message2 as _upgrademessage2

ADDON        = lib.common.ADDON
oldversion = False

class Main:
    def __init__(self):
        linux = False
        packages = []
        if xbmc.getCondVisibility('System.Platform.Linux') and ADDON.getSetting("upgrade_apt") == 'true':
            packages = ['kodi']
            self._versionchecklinux(packages)
        else:
            if ADDON.getSetting("versioncheck_enable") == "true":
                oldversion, version_installed, version_available, version_stable = self._versioncheck()
                if oldversion:
                    self._upgrademessage2( version_installed, version_available, version_stable, oldversion, False)
                else:
                    message_info(32027)

    def _versioncheck(self):
        # initial vars
        from lib.jsoninterface import get_installedversion, get_versionfilelist
        from lib.versions import compare_version
        # retrieve versionlists from supplied version file
        versionlist = get_versionfilelist()
        # retrieve version installed
        version_installed = get_installedversion()
        # copmpare installed and available
        oldversion, version_installed, version_available, version_stable = compare_version(version_installed, versionlist)
        return oldversion, version_installed, version_available, version_stable

    def _versionchecklinux(self,packages):
        import platform
        if platform.dist()[0].lower() in ['ubuntu', 'debian', 'linuxmint']:
            handler = False
            result = False
            try:
                # try aptdeamon first
                from lib.aptdaemonhandler import AptdaemonHandler
                handler = AptdaemonHandler()
            except:
                # fallback to shell
                # since we need the user password, ask to check for new version first
                from lib.shellhandlerapt import ShellHandlerApt
                sudo = False
                if ADDON.getSetting("upgrade_sudo") == "true":
                    sudo = True
                handler = ShellHandlerApt(sudo)
            if handler:
                if ADDON.getSetting("versioncheck_enable") == "true":
                    if handler.check_upgrade_available(packages[0]):
                        message_info(32016)
                        result = handler.upgrade_package(packages[0])
                        if result:
                            from lib.common import message_upgrade_success, message_restart_app
                            message_upgrade_success()
                            message_restart_app()
                        else:
                            log("Abort during upgrade %s" %packages[0],xbmc.LOGERROR)
                            message_info(32029)
                    else:
                        message_info(32027)

                if ADDON.getSetting("upgrade_system") == "true":
                    if handler.check_upgrade_system_available():
                        message_info(32019)
                        result = handler.upgrade_system()
                        if result:
                            from lib.common import message_upgrade_success, message_restart_system
                            message_upgrade_success()
                            message_restart_system()
                        else:
                            log("Abort during upgrade system",xbmc.LOGERROR)
                            message_info(32029)
                    else:
                        message_info(32028)
            else:
                log("Error: no handler found",xbmc.LOGERROR)
                message_info(32029)
        else:
            log("Unsupported platform %s" %platform.dist()[0],xbmc.LOGERROR)
            sys.exit(0)

if (__name__ == "__main__"):
    log('Service started')
    message_info(32026)
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        Main()
        if monitor.waitForAbort(86400):
            log('Bye bye')
            break