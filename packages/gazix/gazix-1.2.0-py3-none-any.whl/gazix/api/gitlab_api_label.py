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

from .gitlab_api_object import *


class GitlLabAPILabel(GitLabAPIObject):

    def __init__(self, name, color, description=None, priority=None, id=-1):
        super().__init__(id)
        self._name = name
        self._color = color
        self._description = description
        self._priority = priority
        self.url()

    def get_type(self):
        return "labels"

    def url(self):
        self._url = "name=" + self._name + "&color=" + self._color
        if self._description is not None:
            self._url += "&description=" + self._description
        if self._priority is not None:
            self._url += "&priority=" + self._priority

    def get_url(self):
        return self._url

    def __str__(self):
        str = "label: " + self._name
        if id != -1:
            str += "\n\tid: " + self._id
        str += "\n\tcolor: " + self._color
        if self._description is not None:
            str += "\n\tdescription: " + self._description
        if self._priority is not None:
            str += "\n\tpriority: " + self._priority
        return str
