#!/usr/bin/python

from be.default import BEProjectRootDirectory
from be.constants import BEPackageType
from be.util import GetLogger

import argparse
import os

from be.configure import GetUserConfig


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
    from be.clean import DoClean
    DoClean()

#if args.target == 'cleanall':
#    from be.cleanall import DoCleanAll
#    DoCleanAll()

if args.target == 'configure':
    from be.configure import DoConfigure
    UserConfig = GetUserConfig(args)
    DoConfigure(UserConfig)

#if args.target == 'dev':
#    DoCompile()
#
#if args.target == 'test':
#    DoCompile()
#    DoTest()
#
#if args.target == 'releaese' or \
#   args.target == 'prelease':
#    DoCompile()
#    DoTest()
#    DoVersion()
#    DoChangeLog()
#    DoUpload()
#    DoEmail()



print args


# __END__
