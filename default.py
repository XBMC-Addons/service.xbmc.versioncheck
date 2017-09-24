############################################################################
#
#  Copyright 2017 Cyr-ius
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################
import xbmcaddon
from lib.common import log, busy,dialog_yesno, set_password
import service

if len(sys.argv) > 1 and sys.argv[1] == "set_password":
	with busy():
		set_password()
else:
	if dialog_yesno(32037):
		log("Started script")
		service.Main()
