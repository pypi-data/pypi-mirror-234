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

class GitLabAPIAccess:

    def __init__(self, gitlab_api_url, token, project):
        self._gitlab_api_url = gitlab_api_url
        self._token = token
        self._project = project

    def is_valid(self):
        return self._gitlab_api_url is not None and self._token is not None and self._project is not None

    def get_url(self):
        return self._gitlab_api_url

    def get_token(self):
        return self._token

    def get_project(self):
        return self._project
