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
from ..arguments.arguments import *
from ..utils.option import *
from ..utils.log import *
from ..api.gitlab_api_pipeline import *

labels_program = "trigger"

_range = 3
_sleep = 60

_range_unstable = 5
_sleep_unstable = 300


class Trigger:

    def __init__(self, arguments):
        self._help = False
        _gitlab_api_url = None
        _token_trigger = None
        _project = None
        self._variables = {}
        self._reference = None
        self._wait = False
        self._unstable = False
        for i in range(len(arguments)):
            if option(arguments[i], gitlab_api_url):
                _gitlab_api_url = arguments[i + 1]
                i += 1
            if option(arguments[i], token_trigger):
                _token_trigger = arguments[i + 1]
                i += 1
            elif option(arguments[i], project):
                _project = arguments[i + 1]
                i += 1
            elif option(arguments[i], variable_short, variable_long):
                key, value = arguments[i + 1].split(":", 1)
                self._variables[key] = value
                i += 1
            elif option(arguments[i], reference_short, reference_long):
                self._reference = arguments[i + 1]
                i += 1
            elif option(arguments[i], wait_short, wait_long):
                self._wait = True
            elif option(arguments[i], unstable_short, unstable_long):
                self._unstable = True
            elif option(arguments[i], help_short, help_long):
                self._help = True
        self._access = GitLabAPIAccess(_gitlab_api_url, _token_trigger, _project)
        self._queries = GitLabAPIQueries(self._access)
        if self._help:
            self.help(gazix, labels_program)
            exit(0)
        if not self._access.is_valid():
            self.help(gazix, labels_program)
            exit(1)
        exit(self.trigger())

    def trigger(self):
        pipeline = self._queries.trigger_pipeline(self._reference, self._variables)
        pipeline_object = GitlLabAPIPipeline(pipeline["id"])
        logger.info("Pipeline triggered... Link: " + pipeline["web_url"])

        r = _range
        s = _sleep

        if self._unstable:
            r = _range_unstable
            s = _sleep_unstable

        if self._wait:
            term = False
            while not term:
                print(".", end="")
                time.sleep(s)
                for i in range(0, r):
                    try:
                        term = self._queries.is_pipeline_terminated(pipeline_object)
                    except:
                        print()
                        print("Impossible to join the pipeline!")
                        if i == 2:
                            print("Connexion failure!")
                            return 2
                        print("Trying again...!")
                        time.sleep(s)
                    else:
                        break
        return 0

    def help(self, gazix="", program=""):
        print(gazix + " " + program + " [options]")
        print("\toptions:")
        print("\t-h/--help                Print the help")
        print("\t--gitlab [value]         Gitlab API url of the repository")
        print("\t--token_trigger [value]  Trigger token of the repository")
        print("\t--project [value]        ID of the repository")
        print("\t-v/--var [key]:[value]   Variable to transmit to the pipeline")
        print("\t-r/--ref [value]         Reference of the repository (main, master, etc.)")
        print("\t-w/--wait                Wait for the end of the pipeline execution")
        print("\t-u/--unstable            Unstable mode")
