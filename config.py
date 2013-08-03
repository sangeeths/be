import logging
from os.path import normpath
from os.path import join


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# USER CONFIGURABLE PARAMETERS for the BUILD ENGINE
#
# Read-Write
#
# Update the value(s) for the following variable(s) 
# to suite the requirement of the project in which 
# the "be" is deployed.
#
#
BEOutputDirectory = '/tmp/be'
#
# The "be" logs would be written to the following file. 
BELogFileName = normpath(join(BEOutputDirectory, 'be.log'))
#
#
# The current log level
BELogLevel = logging.DEBUG
#
#
# The current log format
#BELogFormat = '[%(asctime)s] [%(levelname)-s] ' \
#              '[%(name)s] %(message)s'
BELogFormat = '%(asctime)22s %(levelname)8s  ' \
              '%(name)-12s  $  %(message)s'
#
#
# By default the virtual environment will be created 
# only for 'release' and 'prelease' build targets.
# Other build targets like 'dev' and 'test' will be
# performed in the current working environmet and not
# in a virtual environment. 
# NOTE: If 'dev' and 'test' builds need to executed 
#       in a virtual environment, then please set the
#       "--virtualenv" parameter in "be configure" 
#       command.
BEVirtualEnv = {'dev'      : False, 
                'test'     : False, 
                'release'  : True, 
                'prelease' : True,
               }
#
#
# If user has not configured virtualenv or has not 
# updated the requirements file for virtualenv, but
# if running 'release' and 'prelease' targets,  then
# the following filename will be considered as a 
# requirements file for configuring a virtualenv.
# The following is the (relative) file path to the 
# project root directory.
BERequirements = 'REQUIREMENTS'
#
#
# Base File Name
BEBaseFileName = 'BrightEdge'
#
#
# Target Root
BETargetRoot = '/usr/lib/be/'
#
# End - User Configurable Parameters
# 
# # # # # # # # # # # # # # # # # # # # # # # # #


# __END__
