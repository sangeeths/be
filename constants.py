
# # # # # # # # # # # # # # # # # # # # # # # # #
#
# SYSTEM PARAMETERS
#
# Read-Only
# Do-Not-Disturb
#
Tgz = 'tgz'
Rpm = 'rpm'
#
# The types of packages that are currently supported.
BEPackageType = [Tgz, Rpm]
#
#
# The following are build targets
Tclean     = 'clean'
Tcleanall  = 'cleanall'
Tconfigure = 'configure'
Tdev       = 'dev'
Ttest      = 'test'
Trelease   = 'release'
Tprelease  = 'prelease'
#
#
# The log file name for each and every directory 
# in the build root 
BEConfigFilename               = 'config.be'
BEProjectDefaultConfigFilename = 'default.config.be'
BEProjectConfigureFilename     = 'configure.be'
#
#
# Keys used in the config.be
IgnoreItems = "IgnoreItems"
IgnoreDirNames  = 'IgnoreDirNames'
IgnoreFileNames = 'IgnoreFileNames'
Dependency      = 'Dependency'
AddToPackage    = 'AddToPackage'
#
#
# The following are the parameters that would be
# present in 
#   -> 'default.config.be'
#   -> 'configure.be'
#

Directories  = 'Directories'
Email        = 'Email'
Package      = 'Package'
Tag          = 'Tag'
Verbose      = 'Verbose'
Virtualenv   = 'Virtualenv'
#
#
# The following are the mandatory parameters
# in any build engine config file 
#   -> default.config.be
#   -> configure.be
ConfigMandatoryParams = [
     Directories, 
     Email, 
     Package, 
     Tag, 
     Verbose, 
     Virtualenv,
]
#
#
# When there is no 'BEConfigFilename' in a pwd,
# the following will be considered as a default
# local config file. The default config file is 
# configured to only ignore 'BEConfigFilename'.
# Read-Only
DefaultLocalBEConfig = {IgnoreItems: [BEConfigFilename]}
#
#
# End - System Parameters
# 
# # # # # # # # # # # # # # # # # # # # # # # # #


# __END__
