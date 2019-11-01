# -*- coding: utf-8 -*-

"""

    Copyright (C) 2013-2014 Team-XBMC
    Copyright (C) 2014-2019 Team Kodi

    This file is part of service.xbmc.versioncheck

    SPDX-License-Identifier: GPL-3.0-or-later
    See LICENSES/GPL-3.0-or-later.txt for more information.

"""

from .common import log
from .handler import Handler

try:
    import apt  # pylint: disable=import-error
    from aptdaemon import client  # pylint: disable=import-error
    from aptdaemon import errors  # pylint: disable=import-error
except:
    log('python apt import error')


class AptDaemonHandler(Handler):

    def __init__(self):
        super(AptDaemonHandler, self).__init__()
        self.apt_client = client.AptClient()

    def _check_versions(self, package, update=None):
        if not self._update_cache():
            return False, False
        try:
            trans = self.apt_client.upgrade_packages([package])
            # trans = self.apt_client.upgrade_packages('bla')
            trans.simulate(reply_handler=self._apt_trans_started,
                           error_handler=self._apt_error_handler)
            pkg = trans.packages[4][0]
            if pkg == package:
                cache = apt.Cache()
                cache.open(None)
                cache.upgrade()
                if cache[pkg].installed:
                    return cache[pkg].installed.version, cache[pkg].candidate.version

            return False, False

        except Exception as error:
            log('Exception while checking versions: %s' % error)
            return False, False

    def _update_cache(self):
        try:
            return self.apt_client.update_cache(wait=True) == 'exit-success'
        except errors.NotAuthorizedError:
            log('You are not allowed to update the cache')
            return False

    def upgrade_package(self, package):
        try:
            log('Installing new version')
            if self.apt_client.upgrade_packages([package], wait=True) == 'exit-success':
                log('Upgrade successful')
                return True
        except Exception as error:
            log('Exception during upgrade: %s' % error)
        return False

    def upgrade_system(self):
        try:
            log('Upgrading system')
            if self.apt_client.upgrade_system(wait=True) == 'exit-success':
                return True
        except Exception as error:
            log('Exception during system upgrade: %s' % error)
        return False

    def _apt_trans_started(self):
        pass

    @staticmethod
    def _apt_error_handler(error):
        log('Apt Error %s' % error)
