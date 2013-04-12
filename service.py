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


import os
import platform
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import lib.common
from lib.common import log, message_upgrade_success, message_restart
from lib.common import upgrade_message as _upgrademessage

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__addon__        = lib.common.__addon__
__addonversion__ = lib.common.__addonversion__
__addonname__    = lib.common.__addonname__
__addonpath__    = lib.common.__addonpath__
__icon__         = lib.common.__icon__
__localize__     = lib.common.__localize__


class Main:
    def __init__(self):
        linux = False
        packages = []
        if __addon__.getSetting("versioncheck_enable") == 'true' and not xbmc.getCondVisibility('System.HasAddon(os.openelec.tv)'):
            if not sys.argv[0]:
                xbmc.executebuiltin('XBMC.AlarmClock(CheckAtBoot,XBMC.RunScript(service.xbmc.versioncheck, started),00:00:30,silent)')
                xbmc.executebuiltin('XBMC.AlarmClock(CheckWhileRunning,XBMC.RunScript(service.xbmc.versioncheck, started),24:00:00,silent,loop)')
            elif sys.argv[0] and sys.argv[1] == 'started':
                if xbmc.getCondVisibility('System.Platform.Linux'):
                    packages = ['xbmc']
                    _versionchecklinux(packages)
                else:
                    oldversion, message = _versioncheck()
                    if oldversion:
                        _upgrademessage(message, False)
            else:
                pass
                
def _versioncheck():
    # initial vars
    oldversion = False
    msg = ''
    # retrieve versionlists from supplied version file
    version_file = os.path.join(__addonpath__, 'resources/versions.txt')
    # Eden didn't have xbmcvfs.File()
    if xbmcaddon.Addon('xbmc.addon').getAddonInfo('version') < "11.9.3":
        file = open(version_file, 'r')
    else:
        file = xbmcvfs.File(version_file)
    data = file.read()
    file.close()
    version_query = unicode(data, 'utf-8', errors='ignore')
    version_query = simplejson.loads(version_query)
    
    # Create seperate version lists
    versionlist_stable = version_query['releases']['stable']
    versionlist_rc = version_query['releases']['releasecandidate']
    versionlist_beta = version_query['releases']['beta']
    versionlist_alpha = version_query['releases']['alpha']
    versionlist_prealpha = version_query['releases']['prealpha']        

    # retrieve current installed version
    json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    json_query = simplejson.loads(json_query)
    version_installed = []
    if json_query.has_key('result') and json_query['result'].has_key('version'):
        version_installed  = json_query['result']['version']
        log("Version installed %s" %version_installed)
    # set oldversion flag to false
    oldversion = False

    ### Check to upgrade to newest available stable version
    # check on smaller major version. Smaller version than available always notify
    if version_installed['major'] < int(versionlist_stable[0]['major']):
        msg = __localize__(32003)
        oldversion = True
        log("Version available  %s" %versionlist_stable[0])

    # check on same major version installed and available
    elif version_installed['major'] == int(versionlist_stable[0]['major']):
        # check on smaller minor version
        if version_installed['minor'] < int(versionlist_stable[0]['minor']):
            msg = __localize__(32003)
            oldversion = True
            log("Version available  %s" %versionlist_stable[0])
        # check if not installed a stable so always notify
        elif version_installed['tag'] != "stable":
            msg = __localize__(32008)
            oldversion = True
            log("Version available  %s" %versionlist_stable[0])
        else:
            log("Last available stable installed")

    ### Check to upgrade to newest available RC version if not installed stable
    ## Check also oldversion hasn't been set true by previous check because if so this need to be skipped
    if not oldversion and version_installed['tag'] != "stable":
        # only check on equal or lower major because newer installed beta/alpha/prealpha version will be higher
        if versionlist_rc and version_installed['major'] <= int(versionlist_rc[0]['major']):
            if version_installed['revision'] <= versionlist_rc[0]['revision']:
                msg = __localize__(32004)
                oldversion = True
                log("Version available  %s" %versionlist_rc[0])

        # exclude if installed RC on checking for newer beta
        if not oldversion and versionlist_beta and version_installed['tag'] not in ["releasecandidate"]:
            if version_installed['major'] <= int(versionlist_beta[0]['major']):
                if version_installed['revision'] < versionlist_beta[0]['revision']:
                    msg = __localize__(32005)
                    oldversion = True
                    log("Version available  %s" %versionlist_beta[0])
    
        # exclude if installed RC or beta on checking for newer alpha
        if not oldversion and versionlist_alpha and version_installed['tag'] not in ["releasecandidate", "beta"]:
            if version_installed['major'] <= int(versionlist_alpha[0]['major']):
                if version_installed['revision'] < versionlist_alpha[0]['revision']:
                    msg = __localize__(32006)
                    oldversion = True
                    log("Version available  %s" %versionlist_alpha[0])

        # exclude if installed RC, beta or alpha on checking for newer prealpha
        if not oldversion and versionlist_prealpha and version_installed['tag'] not in ["releasecandidate", "beta", "alpha"]:
            if version_installed['major'] <= int(versionlist_prealpha[0]['major']):
                if version_installed['revision'] < versionlist_prealpha[0]['revision']:
                    msg = __localize__(32007)
                    oldversion = True
                    log("Version available  %s" %versionlist_prealpha[0])

        # Nothing to see here, move along
    else:
        # Nothing to see here, move along
        pass
    return oldversion, msg


def _versionchecklinux(packages):
    if (platform.dist()[0] == "Ubuntu" or platform.dist()[0] == "Debian"):
        try:
            # try aptdeamon first
            from lib.aptdeamonhandler import AptdeamonHandler
            handler = AptdeamonHandler()
        except:
            # fallback to shell
            # since we need the user password, ask to check for new version first
            if _upgrademessage(__localize__(32015), True):
                from lib.shellhandlerapt import ShellHandlerApt
                sudo = True
                handler = ShellHandlerApt(sudo)

    else:
        log("Unsupported platform %s" %platform.dist()[0])
        sys.exit(0)

    if handler:
        if handler.check_upgrade_available(packages[0]):
            if _upgrademessage(__localize__(32012), True):
                if handler.upgrade_package(packages[0]): 
                    message_upgrade_success()
                    message_restart()
    else:
        log("Error: no handler found")



if (__name__ == "__main__"):
    log('Version %s started' % __addonversion__)
    Main()
