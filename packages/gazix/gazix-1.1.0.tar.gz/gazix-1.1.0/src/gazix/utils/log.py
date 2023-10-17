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
import time
import os
import getpass

logging_context = "gazix"
#Initializing logger
#if not(os.path.isdir("gazix-log")):
#	os.system("mkdir gazix-log")
#os.system("rm -f gazix-log/*")

logger = logging.getLogger(logging_context)
date = time.strftime("%Y_%m_%d_%H")
user = getpass.getuser()
#fh = logging.FileHandler('gazix-log/'+date+'.log')

#Logger set debug level
logger.setLevel(logging.INFO)
#fh.setLevel(logging.DEBUG)

#Set logger format
formatter = logging.Formatter('[%(asctime)s] [%(funcName)s():%(lineno)d] %(levelname)s - %(message)s','%m-%d %H:%M:%S')
#fh.setFormatter(formatter)
#logger.addHandler(fh)
