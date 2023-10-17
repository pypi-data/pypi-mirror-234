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

class GitLabAPIObject:

    def __init__(self, id=-1):
        self._url = None
        self._id = id

    def get_id(self):
        return id

    def get_type(self):
        return None

    def url(self):
        self._url = None

    def get_url(self):
        return self._url

    def get_query(self):
        return str(self._id)

    def __str__(self):
        return None
