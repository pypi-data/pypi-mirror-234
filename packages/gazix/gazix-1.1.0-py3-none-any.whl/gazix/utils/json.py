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

# -*- coding: utf-8 -*-
import json
import os


def exist_json(name):
    """
       Test if Json file exist
    """
    return os.path.isfile(name)


def open_json(name):
    """
        Open a Json file.
    """
    with open(name) as json_data:
        d = json.load(json_data)
    return d


def read_json(string):
    return json.loads(string)


def save_json(d, name):
    with open(name, 'w') as fp:
        json.dump(d, fp, indent=4, sort_keys=True)
