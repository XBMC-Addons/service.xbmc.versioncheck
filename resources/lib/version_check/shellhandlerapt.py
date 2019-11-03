# -*- coding: utf-8 -*-

"""

    Copyright (C) 2013-2014 Team-XBMC
    Copyright (C) 2014-2019 Team Kodi

    This file is part of service.xbmc.versioncheck

    SPDX-License-Identifier: GPL-3.0-or-later
    See LICENSES/GPL-3.0-or-later.txt for more information.

"""

import sys

from .common import get_password_from_user
from .common import log

try:
    from subprocess import check_output
    from subprocess import call
except:
    log('subprocess import error')


class ShellHandlerApt:
    _pwd = ''

    def __init__(self, usesudo=False):
        self.sudo = usesudo
        installed, candidate = self._check_versions('xbmc', False)
        if not installed:
            # there is no package installed via repo, so we exit here
            log('No installed package found, exiting')
            sys.exit(0)

    def _check_versions(self, package, update=True):
        _cmd = 'apt-cache policy ' + package

        if update and not self._update_cache():
            return False, False

        try:
            result = check_output([_cmd], shell=True).split('\n')
        except Exception as error:
            log('ShellHandlerApt: exception while executing shell command %s: %s' % (_cmd, error))
            return False, False

        if result[0].replace(':', '') == package:
            installed = result[1].split()[1]
            candidate = result[2].split()[1]
            if installed == '(none)':
                installed = False
            if candidate == '(none)':
                candidate = False
            return installed, candidate
        else:
            log('ShellHandlerApt: error during version check')
            return False, False

    def _update_cache(self):
        _cmd = 'apt-get update'
        try:
            if self.sudo:
                x = check_output('echo \'%s\' | sudo -S %s' % (self._getpassword(), _cmd), shell=True)
            else:
                x = check_output(_cmd.split())
        except Exception as error:
            log('Exception while executing shell command %s: %s' % (_cmd, error))
            return False

        return True

    def check_upgrade_available(self, package):
        '''returns True if newer package is available in the repositories'''
        installed, candidate = self._check_versions(package)
        if installed and candidate:
            if installed != candidate:
                log('Version installed  %s' % installed)
                log('Version available  %s' % candidate)
                return True
            else:
                log('Already on newest version')
        elif not installed:
            log('No installed package found')
            return False
        else:
            return False

    def upgrade_package(self, package):
        _cmd = 'apt-get install -y ' + package
        try:
            if self.sudo:
                x = check_output('echo \'%s\' | sudo -S %s' % (self._getpassword(), _cmd), shell=True)
            else:
                x = check_output(_cmd.split())
            log('Upgrade successful')
        except Exception as error:
            log('Exception while executing shell command %s: %s' % (_cmd, error))
            return False

        return True

    def upgrade_system(self):
        _cmd = 'apt-get upgrade -y'
        try:
            log('Upgrading system')
            if self.sudo:
                x = check_output('echo \'%s\' | sudo -S %s' % (self._getpassword(), _cmd), shell=True)
            else:
                x = check_output(_cmd.split())
        except Exception as error:
            log('Exception while executing shell command %s: %s' % (_cmd, error))
            return False

        return True

    def _getpassword(self):
        if len(self._pwd) == 0:
            self._pwd = get_password_from_user()
        return self._pwd
