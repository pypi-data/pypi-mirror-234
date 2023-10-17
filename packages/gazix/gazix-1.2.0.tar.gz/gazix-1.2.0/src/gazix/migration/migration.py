#########################################################################
#                                                                       #
#  This file is part of gazix.                                          #
#                                                                       #
#  gazix is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by #
#  the Free Software Foundation, either version 3 of the License, or    #
#  (at your option) any later version.                                  #
#                                                                       #
#  gazix is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of       #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        # 
#  GNU General Public License for more details.                         #
#                                                                       #
#  You should have received a copy of the GNU General Public License    #
#  along with gazix. If not, see <https://www.gnu.org/licenses/>.       #
#                                                                       #
#########################################################################

from ..api.gitlab_api_access import *
from ..api.gitlab_api_queries import *
from ..utils.option import *
from ..arguments.arguments import *


class Migration:

    def __init__(self, arguments):
        self._help = False
        _gitlab_api_url_src = None
        _token_src = None
        _project_src = None
        _gitlab_api_url_target = None
        _token_target = None
        _project_target = None
        for i in range(len(arguments)):
            if option(arguments[i], gitlab_api_url_src):
                _gitlab_api_url_src = arguments[i + 1]
                i += 1
            elif option(arguments[i], gitlab_api_url_target):
                _gitlab_api_url_target = arguments[i + 1]
                i += 1
            if option(arguments[i], token_src):
                _token_src = arguments[i + 1]
                i += 1
            elif option(arguments[i], token_target):
                _token_target = arguments[i + 1]
                i += 1
            elif option(arguments[i], project_src):
                _project_src = arguments[i + 1]
                i += 1
            elif option(arguments[i], project_target):
                _project_target = arguments[i + 1]
                i += 1
            elif option(arguments[i], help_short, help_long):
                self._help = True
        self._access_src = GitLabAPIAccess(_gitlab_api_url_src, _token_src, _project_src)
        self._access_target = GitLabAPIAccess(_gitlab_api_url_target, _token_target, _project_target)
        self._queries_src = GitLabAPIQueries(self._access_src)
        self._queries_target = GitLabAPIQueries(self._access_target)

    def help(self, gazix="", program=""):
        print(gazix + " " + program + " [options]")
        print("\toptions:")
        print("\t--help            Print the help")
        print("\t--gitlab_src      Gitlab API url of the source repository")
        print("\t--gitlab_target   Gitlab API url of the target repository")
        print("\t--token_src       Access token of the source repository")
        print("\t--token_target    Access token of the target repository")
        print("\t--project_src     ID of the source repository")
        print("\t--project_target  ID token of the target repository")
