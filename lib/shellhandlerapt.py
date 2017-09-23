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
from common import *

try:
    from subprocess import check_output
    from subprocess import call
except Exception as error:
    log('subprocess import error :%s' %error,xbmc.LOGERROR)

class ShellHandlerApt:

    _pwd = ""

    def __init__(self, usesudo=False):
        log("Handler is Shell")
        self.sudo = usesudo
        installed, candidate = self._check_versions("xbmc", False)
        if not installed:
            # there is no package installed via repo, so we exit here
            log("No installed package found, exiting")
            import sys
            sys.exit(0)

    def _check_versions(self, package, update=True):
        _cmd = "apt-cache policy " + package

        if update and not self._update_cache():
            return False, False

        try:
            result = check_output([_cmd], shell=True).split("\n")
        except Exception as error:
            log("ShellHandlerApt: exception while executing shell command %s: %s" %(_cmd, error),xbmc.LOGERROR)
            return False, False

        if result[0].replace(":", "") == package:
            installed = result[1].split()[1]
            candidate = result[2].split()[1]
            if installed == "(none)":
                installed = False
            if candidate == "(none)":
                candidate = False
            return installed, candidate
        else:
            log("ShellHandlerApt: error during version check")
            return False, False

    def _update_cache(self):
        _cmd = 'apt-get update'
        try:
            if self.sudo:
                log("Update cache [SUDO]")
                x = check_output('echo \'%s\' | sudo -S %s' %(get_password(), _cmd), shell=True)
            else:
                log("Update cache")
                x = check_output(_cmd.split())
        except Exception as error:
            log("Exception while executing shell command %s: %s" %(_cmd, error),xbmc.LOGERROR)
            return False
        log(x)
        return True

    def check_upgrade_available(self, package):
        '''returns True if newer package is available in the repositories'''
        installed, candidate = self._check_versions(package)
        if installed and candidate:
            if installed != candidate:
                log("Version installed  %s" %installed)
                log("Version available  %s" %candidate)
                return True
            else:
                log("Already on newest version for %s" %package)
        elif not installed:
                log("No installed package found for %s" %package)
                return False
        else:
            return False

    def upgrade_package(self, package):
        _cmd = "apt-get install -y " + package
        try:
            if self.sudo:
                x = check_output('echo \'%s\' | sudo -S %s' %(get_password(), _cmd), shell=True)
            else:
                x = check_output(_cmd.split())
            log("Install package %s successful" %package,True)
        except Exception as error:
            log("Exception while executing shell command %s: %s" %(_cmd, error),xbmc.LOGERROR)
            return False

        return True

    def check_upgrade_system_available(self):
        _cmd = "apt list --upgradable"
        try:
            if self._update_cache():
                if self.sudo:
                    x = check_output('echo \'%s\' | sudo -S %s' %(get_password(), _cmd), shell=True)
                else:
                    x = check_output(_cmd.split())
                n = len(x.splitlines())
                if (n > 1):
                    log("Upgrade system available")
                    return True
            log("No system update available")
            return False
        except Exception as error:
            log("Exception while executing shell command %s: %s" %(_cmd, error),xbmc.LOGERROR)
            return False

    def upgrade_system(self):
        _cmd = "apt-get dist-upgrade -y"
        try:
            if not dialog_yesno(32018):
                return False
            dialog = xbmcgui.DialogBusy()
            dialog.create()
            if self.sudo:
                x = check_output('echo \'%s\' | sudo -S %s' %(get_password(), _cmd), shell=True)
            else:
                x = check_output(_cmd.split())
            dialog.close()
            log("Upgrade System successful")
        except Exception as error:
            log("Exception while executing shell command %s: %s" %(_cmd, error),xbmc.LOGERROR)
            return False

        return True
