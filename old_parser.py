#!/usr/bin/python

from be.util import GetLogger

import argparse

logger = GetLogger(__name__)



desc = "This is a description..."

#parser = argparse.ArgumentParser(description=desc)


parser = argparse.ArgumentParser(add_help=False)

target = parser.add_mutually_exclusive_group(required=True)

help_clean     = 'clean all system generated build files (*.pyc).'
help_configure = '[step-1] configure the build engine.'
help_dev       = 'build the source directory.'
help_rel       = 'build the source directory, run the unit tests, ' \
                 'update version, package, generate change logs, ' \
                 'generate python docs, upload to hosting server ' \
                 'and send an email to the group'
help_prelease  = '%s: %s' % ('production release', help_rel)
help_release   = '%s: %s' % ('development release (internal)', help_rel)
help_test      = 'build the source directory and run the unit tests.'

target.add_argument('--clean',     action='store_true', help=help_clean)
target.add_argument('--configure', action='store_true', help=help_configure)
target.add_argument('--dev',       action='store_true', help=help_dev)
target.add_argument('--test',      action='store_true', help=help_test)
target.add_argument('--release',   action='store_true', help=help_release)
target.add_argument('--prelease',  action='store_true', help=help_prelease)



help_conf_parser = 'the following options are applicable only for ' \
                   '\"--configure\" target. if these options are ' \
                   'entered for other build targets, they will be ' \
                   'discarded.'
help_dirs    = 'enter the list of directories to be compiled. ' \
               '[default] when left blank, all directories will ' \
               'be compiled.'
help_package = 'enter the pagckage type. [default] when left blank, ' \
               'all (tgz and rpm) packages will be made.'
help_tag     = 'enter a tag which will be added to the build output ' \
               'package file name.'
help_email   = 'enter an email address to which the build report ' \
               'should be sent.'
help_verbose = 'the build logs will be printed in the stdout ' \
               '[default = False]'
help_logfile = 'where do you want the build logs to go? ' \
               '[default = /a/b/c/d]'
#help_venv    = 'create a virtual environment to perform the build ' \
#               '[default = False (\"dev\", \"test\"); True (\"release\"' \
#               ', \"prelease\")]'
#help_req     = 'path to the requirement file which captures the ' \
#               'dependency python packages to be installed in the ' \
#               'virtual environment. this is applicable only when ' \
#               '\"-V\"/\"--virtualenv\" is True; otherwise ignored.'
#help_rdir    = 'path to the project root directory.'



configure = parser.add_argument_group('configure', help_conf_parser)

configure.add_argument('-d', '--dirs', help=help_dirs, nargs='+')
configure.add_argument('-p', '--package', help=help_package, 
                       nargs='+', choices=['tgz', 'rpm'])
configure.add_argument('-t', '--tag', help=help_tag)
configure.add_argument('-e', '--email', help=help_email)
configure.add_argument('-v', '--verbose', help=help_verbose, 
                       action='store_true', default=False)
configure.add_argument('-l', '--logfile',     help=help_logfile) 
#configure.add_argument('-V', '--virtualenv',  help=help_venv) 
#configure.add_argument('-r', '--requirement', help=help_req) 
#configure.add_argument('-R', '--rootdir',     help=help_rdir) 

args = parser.parse_args()

msg = 'The parsed arguments : %s' % args
logger.debug(msg)

print dir(args)

def IgnoreConfigureParams(args):
    if not args.configure:
        if args.dirs:
            logger.warning('Ignoring dirs [%s] as it is not applicable to the current context' % ', '.join(args.dirs))
        if args.package:
            logger.warning('Ignoring package [%s] as it is not applicable to the current context' % ', '.join(args.package))
#        if args.tag:
#        if args.email:
#        if args.verbose:
#        if args.logfile:

    return

IgnoreConfigureParams(args)

if args.configure:
    pass

if args.clean:
    pass

if args.dev:
    pass

if args.test:
    pass

if args.release:
    pass

if args.prelease:
    pass


print args
print args.dirs
print args.package
print args.tag
print args.email
print args.verbose
print '===================================='
parser.print_help()


