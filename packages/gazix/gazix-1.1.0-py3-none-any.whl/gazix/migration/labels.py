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

import logging

from .migration import *
from ..arguments.arguments import *
from ..api.gitlab_api_label import *
from ..utils.log import *

labels_program = "cp-labels"


def list_labels(queries):
    label_dict = queries.list_labels()
    logging.debug(label_dict)
    labels = {}
    for lab in label_dict:
        name = lab["name"]
        color = lab["color"]
        description = lab["description"]
        priority = lab["priority"]
        labels[name] = GitlLabAPILabel(name, color, description, priority)
        logger.debug(labels[name])
    return labels


class Labels(Migration):

    def __init__(self, arguments):
        super().__init__(arguments)
        if self._help:
            self.help(gazix, labels_program)
            exit(0)
        if not self._access_src.is_valid() or not self._access_target.is_valid():
            self.help(gazix, labels_program)
            exit(1)
        self.add_missing_labels()

    def add_missing_labels(self):
        labels_src = list_labels(self._queries_src)
        labels_target = list_labels(self._queries_target)
        for lab in labels_src:
            if lab not in labels_target:
                logger.debug(lab + " not in target")
                json = self._queries_target.create(labels_src[lab])
                logger.debug(json)
            else:
                logger.debug(lab + " in target")



