# -*- coding: utf-8 -*-

"""

    Copyright (C) 2013-2014 Team-XBMC
    Copyright (C) 2014-2019 Team Kodi

    This file is part of service.xbmc.versioncheck

    SPDX-License-Identifier: GPL-3.0-or-later
    See LICENSES/GPL-3.0-or-later.txt for more information.

"""

from .common import log


# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def compare_version(version_installed, version_list):
    # Create separate version lists
    version_list_stable = version_list['releases']['stable']
    version_list_rc = version_list['releases']['releasecandidate']
    version_list_beta = version_list['releases']['beta']
    version_list_alpha = version_list['releases']['alpha']
    # version_list_prealpha = version_list['releases']['prealpha']
    log('Version installed %s' % version_installed)
    # Check to upgrade to newest available stable version
    # check on smaller major version. Smaller version than available always notify
    old_version = False
    version_available = ''
    # check if installed major version is smaller than available major stable
    # here we don't care if running non stable
    if version_installed['major'] < int(version_list_stable[0]['major']):
        version_available = version_list_stable[0]
        old_version = 'stable'
        log('Version available  %s' % version_list_stable[0])
        log('You are running an older version')

    # check if installed major version is equal than available major stable
    # however also check on minor version and still don't care about non stable
    elif version_installed['major'] == int(version_list_stable[0]['major']):
        if version_installed['minor'] < int(version_list_stable[0]['minor']):
            version_available = version_list_stable[0]
            old_version = 'stable'
            log('Version available  %s' % version_list_stable[0])
            log('You are running an older minor version')
        # check for <= minor !stable
        elif version_installed['tag'] != 'stable' and \
                version_installed['minor'] <= int(version_list_stable[0]['minor']):
            version_available = version_list_stable[0]
            old_version = True
            log('Version available  %s' % version_list_stable[0])
            log('You are running an older non stable minor version')
        else:
            log('Version available  %s' % version_list_stable[0])
            log('There is no newer stable available')

    # Already skipped a possible newer stable build. Let's continue with non stable builds.
    # Check also 'old_version' hasn't been set to 'stable' or true by previous checks because
    # if so, those part need to be skipped

    # check for RC builds
    if not old_version and version_installed['tag'] in ['releasecandidate']:
        # check if you are using a RC build lower than current available RC
        # then check if you are using a beta/alpha lower than current available RC
        # 14.0rc3 is newer than:  14.0rc1, 14.0b9, 14.0a15
        if version_installed['major'] <= int(version_list_rc[0]['major']):
            if version_installed['minor'] <= int(version_list_rc[0]['minor']):
                if version_installed.get('tagversion', '') < version_list_rc[0]['tagversion']:
                    version_available = version_list_rc[0]
                    old_version = True
                    log('Version available  %s' % version_list_rc[0])
                    log('You are running an older RC version')
    # now check if installed !=rc
    elif not old_version and version_installed['tag'] in ['beta', 'alpha', 'prealpha']:
        if version_installed['major'] <= int(version_list_rc[0]['major']):
            if version_installed['minor'] <= int(version_list_beta[0]['minor']):
                version_available = version_list_rc[0]
                old_version = True
                log('Version available  %s' % version_list_rc[0])
                log('You are running an older non RC version')

    # check for beta builds
    if not old_version and version_installed['tag'] == 'beta':
        # check if you are using a RC build lower than current available RC
        # then check if you are using a beta/alpha lower than current available RC
        # 14.0b3 is newer than:  14.0b1, 14.0a15
        if version_installed['major'] <= int(version_list_beta[0]['major']):
            if version_installed['minor'] <= int(version_list_beta[0]['minor']):
                if version_installed.get('tagversion', '') < version_list_beta[0]['tagversion']:
                    version_available = version_list_beta[0]
                    old_version = True
                    log('Version available  %s' % version_list_beta[0])
                    log('You are running an older beta version')
    # now check if installed !=beta
    elif not old_version and version_installed['tag'] in ['alpha', 'prealpha']:
        if version_installed['major'] <= int(version_list_beta[0]['major']):
            if version_installed['minor'] <= int(version_list_beta[0]['minor']):
                version_available = version_list_beta[0]
                old_version = True
                log('Version available  %s' % version_list_beta[0])
                log('You are running an older non beta version')

    # check for alpha builds and older
    if not old_version and version_installed['tag'] == 'alpha':
        # check if you are using a RC build lower than current available RC
        # then check if you are using a beta/alpha lower than current available RC
        # 14.0a3 is newer than: 14.0a1 or pre-alpha
        if version_installed['major'] <= int(version_list_alpha[0]['major']):
            if version_installed['minor'] <= int(version_list_alpha[0]['minor']):
                if version_installed.get('tagversion', '') < version_list_alpha[0]['tagversion']:
                    version_available = version_list_alpha[0]
                    old_version = True
                    log('Version available  %s' % version_list_alpha[0])
                    log('You are running an older alpha version')
    # now check if installed !=alpha
    elif not old_version and version_installed['tag'] in ['prealpha']:
        if version_installed['major'] <= int(version_list_alpha[0]['major']):
            if version_installed['minor'] <= int(version_list_alpha[0]['minor']):
                version_available = version_list_alpha[0]
                old_version = True
                log('Version available  %s' % version_list_alpha[0])
                log('You are running an older non alpha version')
    version_stable = version_list_stable[0]
    return old_version, version_installed, version_available, version_stable
