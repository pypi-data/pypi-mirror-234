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

import sys
from .utils.option import option
from .migration.labels import Labels
from .trigger.trigger import Trigger
from .kill.kill_old import KillOld

def help():
    print("gazix [option]")
    print("\toption:")
    print("\thelp          Print the help")
    #print("\tcp-MR         Copy all the merge requests from a source to a target repositories")
    #print("\tcp-issues     Copy all the issues from a source to a target repositories")
    print("\tcp-labels     Copy all the labels from a source to a target repositories")
    print("\ttrigger       Trigger the pipeline of a target repository")
    print("\tkill-old      Kill the old running pipelines of a MR")


def main():
    program = None
    try:
        program = sys.argv[1]
        status = "help" in program
        if status:
            raise Exception
    except:
        help()
        exit()
    try:
        args = sys.argv[2:]
    except:
        args = None
    if option(program, "cp-labels"):
        Labels(args)
    if option(program, "trigger"):
        Trigger(args)
    if option(program, "kill-old"):
        KillOld(args)


if __name__ == "__main__":
    main()
