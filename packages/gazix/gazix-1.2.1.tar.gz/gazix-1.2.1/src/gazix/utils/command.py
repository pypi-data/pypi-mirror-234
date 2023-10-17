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
import os
import subprocess as subp
import signal


def command(line, stdout=False, output=False, timeout=1200):
    """
        Execute a shell command
    """
    if output:
        stdout = True

    if not stdout:
        line += ""

    if output:
        line += ""
        output = ""
        try:
            p = subp.Popen(line,
                           stdout=subp.PIPE,
                           stderr=subp.STDOUT,
                           shell=True)

            output, err = p.communicate(timeout=timeout)
        except subp.TimeoutExpired:
            os.kill(p.pid, signal.SIGTERM)
            output, err = p.communicate()
            return output.decode('utf-8')+"\nEXECUTION TIME OUT"
        else:
            return output.decode('utf-8')
    try:
        p = subp.Popen(line, stdout=subp.PIPE, shell=True, stderr=subp.PIPE)
        output, err = p.communicate(timeout=timeout)
    except subp.TimeoutExpired:
        os.kill(p.pid, signal.SIGTERM)
        return False
    else:
        if p.returncode != 0:
            return False
    return True


def critical_command(line):
    err = subp.call([line+" > /dev/null 2>&1 "], shell=True)
    if err:
        raise RuntimeError("An error has been detected during the " +
                           "execution of: " + line)
    return True

