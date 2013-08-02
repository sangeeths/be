#!/usr/bin/python

from be.default import BEProjectRootDirectory
from be.constants import BEPackageType
from be.util import GetLogger

import argparse
import os

from be.constants import BEProjectDefaultConfigFilename

from be.validation import GetAbsPath
from be.validation import GetEmails
from be.validation import GetPackages
from be.validation import ValidTag
from be.validation import ValidVirtualEnvReqFile

logger = GetLogger(__name__)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
#                Build System Help String Constants
#
# Targets
#
help_clean      = 'cleans the system generated build files (*.pyc).'
help_cleanall   = 'cleans all the system generated build files ' \
                  'including build configure information and *.pyc\'s,'
help_configure  = '[step-1] configure the build engine.'
help_dev        = 'build the source directory.'
help_rel        = 'build the source directory, run the unit tests, ' \
                  'update version, package, generate change logs, ' \
                  'generate python docs, upload to hosting server ' \
                  'and send an email to the group'
help_prelease   = '%s: %s' % ('production release', help_rel)
help_release    = '%s: %s' % ('development release (internal)', help_rel)
help_test       = 'build the source directory and run the unit tests.'
#
# Configure Options
#
help_dirs       = 'enter the list of directories to be compiled. ' \
                  '[default] when left blank, all directories will ' \
                  'be compiled.'
help_package    = 'enter the pagckage type. [default] when left blank, ' \
                  'all (tgz and rpm) packages will be made.'
help_tag        = 'enter a tag which will be added to the build output ' \
                  'package file name.'
help_email      = 'enter an email address to which the build report ' \
                  'should be sent.'
help_verbose    = 'the build logs will be printed in the stdout ' \
                  '[default = False]'
help_venv       = 'do you want this build to be performed in a ' \
                  'virtual environment? [default = False]'
#
#
# End - help strings
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# Create the top-level parser
parser = argparse.ArgumentParser()

# Create the handler for sub-parsers
subparsers = parser.add_subparsers(help='build targets', dest='target')


# Sub-parser for sub-command 'clean'
parser_clean = subparsers.add_parser('clean', help=help_clean)

# Sub-parser for sub-command 'cleanall'
parser_cleanall = subparsers.add_parser('cleanall', help=help_cleanall)

# Sub-parser for sub-command 'configure'
parser_configure = subparsers.add_parser('configure', help=help_configure)

# Arguments for sub-command 'configure'
parser_configure.add_argument('-d', '--dirs',       help=help_dirs, 
                                                    nargs='+')
parser_configure.add_argument('-p', '--package',    help=help_package, 
                                                    nargs='+', 
                                                    choices=list(BEPackageType._keys))
parser_configure.add_argument('-t', '--tag',        help=help_tag)
parser_configure.add_argument('-e', '--email',      help=help_email,
                                                    nargs='+')
parser_configure.add_argument('-v', '--verbose',    help=help_verbose, 
                                                    action='store_true', 
                                                    default=False)
parser_configure.add_argument('-V', '--virtualenv', help=help_venv, 
                                                    metavar='REQUIREMENTS')

# Sub-parser for sub-command 'dev'
parser_dev = subparsers.add_parser('dev', help=help_dev)

# Sub-parser for sub-command 'test'
parser_test = subparsers.add_parser('test', help=help_test)

# Sub-parser for sub-command 'release'
parser_release = subparsers.add_parser('release', help=help_release)

# Sub-parser for sub-command 'prelease'
parser_prelease = subparsers.add_parser('prelease', help=help_prelease)


# Parse the command line arguments using the parser
args = parser.parse_args()







if args.target == 'clean':
    pass
if args.target == 'cleanall':
    pass

if args.target == 'configure':
    from be.constants import Directories
    from be.constants import Email
    from be.constants import Package
    from be.constants import Tag
    from be.constants import Verbose
    from be.constants import Virtualenv
    from be.dparams import DParams
    from be.configure import DoConfigure

    logger.debug('The following are the default parameters')
    logger.debug(DParams)

    logger.debug('Preparing to read the configure parameters')
    UserConfig = DParams

    if args.dirs:
        old = UserConfig[Directories]
        UserConfig[Directories] = GetAbsPath(args.dirs)
        msg = 'Updated Directories From %s To %s' % \
              (old, UserConfig[Directories])
        logger.debug(msg)

    if args.email:
        old = UserConfig[Email]
        UserConfig[Email] = GetEmails(args.email)
        msg = 'Updated Emails From %s To %s' % \
              (old, UserConfig[Email])
        logger.debug(msg)

    if args.package:
        old = UserConfig[Package]
        UserConfig[Package] = GetPackages(args.package)
        msg = 'Updated Packages From %s To %s' % \
              (old, UserConfig[Package])
        logger.debug(msg)

    if args.tag:
        old = UserConfig[Tag]
        ValidTag(args.tag)
        UserConfig[Tag] = args.tag
        msg = 'Updated Tag From [%s] To [%s]' % \
              (old, UserConfig[Tag])
        logger.debug(msg)

    if args.verbose:
        old = UserConfig[Verbose]
        UserConfig[Verbose] = args.verbose
        msg = 'Updated Verbose From %s To %s' % \
              (old, UserConfig[Verbose])
        logger.debug(msg)

    if args.virtualenv:
        old = UserConfig[Virtualenv]
        ValidVirtualEnvReqFile(args.virtualenv)
        UserConfig[Virtualenv] = args.virtualenv
        msg = 'Updated VirtualEnv Requirements From [%s] To [%s]' % \
              (old, UserConfig[Virtualenv])
        logger.debug(msg)

    logger.debug(" final Configuration : ")
    logger.debug(UserConfig)

    #DoConfigure(UserConfig)



if args.target == 'dev':
    pass
if args.target == 'test':
    pass
if args.target == 'releaese':
    pass
if args.target == 'preleaese':
    pass




print args

## parse some argument lists
#parser.parse_args(['a', '12'])
#parser.parse_args(['--foo', 'b', '--baz', 'Z'])


