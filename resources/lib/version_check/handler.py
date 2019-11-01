# -*- coding: utf-8 -*-

"""

    Copyright (C) 2019 Team Kodi

    This file is part of service.xbmc.versioncheck

    SPDX-License-Identifier: GPL-3.0-or-later
    See LICENSES/GPL-3.0-or-later.txt for more information.

"""

from .common import get_password_from_user
from .common import log


class Handler:

    def __init__(self):
        self._pwd = ''

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, value):
        self._pwd = value

    def _check_versions(self, package, update=True):
        raise NotImplementedError

    def check_upgrade_available(self, package):
        """
            returns True if newer package is available in the repositories
        """

        installed, candidate = self._check_versions(package)
        if installed and candidate:
            if installed != candidate:
                log('Version installed  %s' % installed)
                log('Version available  %s' % candidate)
                return True
            log('Already on newest version')
            return False

        if not installed:
            log('No installed package found')

        return False

    def _get_password(self):
        if not self.pwd:
            self.pwd = get_password_from_user()
        return self.pwd
