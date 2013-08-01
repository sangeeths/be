from enum import Enum
import logging


# # # # # # # # # # # # # # # # # # # # # # # # #
#
# SYSTEM PARAMETERS
#
# Read-Only
# Do-Not-Disturb
#
#
# The types of packages that are currently supported.
BEPackageType = Enum('tgz', 'rpm')
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
# The log file name for each and every directory 
# in the build root 
BEConfigFilename = 'config.be'
#
#
# Keys used in the config.be
IgnoreDirNames  = 'IgnoreDirNames'
IgnoreFileNames = 'IgnoreFileNames'
#
#
# When there is no 'BEConfigFilename' in a pwd,
# the following will be considered as a default
# local config file. The default config file is 
# configured to only ignore 'BEConfigFilename'.
# Read-Only
DefaultLocalBEConfig = {IgnoreFileNames: [BEConfigFilename]}
#
#
# End - System Parameters
# 
# # # # # # # # # # # # # # # # # # # # # # # # #


# __END__
