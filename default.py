from os.path import join, normpath
from be.constants import BEPackageType


# # # # # # # # # # # # # # # # # # # # # # # # #
#
# USER CONFIGURABLE PARAMETERS
#
# Read-Write
#
# Update the value(s) for the following variable(s) 
# to suite the requirement # of the project in which 
# the "be" is # deployed.
#
#
# This is the root directory for the project where 
# "be" is deployed.
#BEProjectRootDirectory = '/home/sangeeth/trials/build/dir1'
BEProjectRootDirectory = '/home/sangeeth/riptideio/be/brightedge'
#
#
# Where do you want your .pyc files to go?! When 
# this variable is empty (i.e. ''), the .pyc files 
# will be put in the BEProjectRootDirectory.
BEPrefix = '/tmp/building.be'
#
#
# The "be" logs would be written to the following file. 
BELogFileName = '/tmp/output.be'
#
#
# These are the list of directories that has to be 
# considered for compilation. The directories that 
# are listed here should be relative to the 
# "BEProjectRootDirectory". If this list is empty 
# (default) then all the directories would be 
# considered for compilation.
BEModule = []
#
#
# How do you want the compiled files to be packaged?
# Add the package types to the list.
BEPackage = [BEPackageType.tgz, BEPackageType.rpm]
#
#
# Non functional argument. The "tag" will just get
# added to the packaged file name. Example tags are 
# "weekly", "monthly", etc.
BETag = ''
#
#
# The build summary would be sent to this email id
# when present. When empty, no email will be sent.
BEEmail = ''
#
#
# Do you want the build logs to print on the stdout?!
BEVerbose = True
#
#
# Do you want this build to be performed in a 
# virtual environment?!
BEVirtualEnv = False
#
#
# The path (with name) to the REQUIREMENTS file. This
# file is read and all the required python packages 
# are installed (using easy_install or pip) in the 
# virtual environment where the build would be done.
BERequirements = normpath(join(BEProjectRootDirectory, 
                               'REQUIREMENTS'))
#
#
# End - User Configurable Parameters
# 
# # # # # # # # # # # # # # # # # # # # # # # # #


# __END__
