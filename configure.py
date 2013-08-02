from be.constants import BEProjectConfigureFilename
from be.constants import Directories
from be.constants import Email
from be.constants import Package
from be.constants import Tag
from be.constants import Verbose
from be.constants import Virtualenv

from be.validation import GetAbsPath
from be.validation import GetEmails
from be.validation import GetPackages
from be.validation import ValidTag
from be.validation import ValidVirtualEnvReqFile

from be.cparams import CParams    

from be.exception import ConfigureFailed

from be.util import GetLogger

from datetime import datetime

from os import remove
from os.path import isfile

import json


logger = GetLogger(__name__)


def DoConfigure(args):

    if isfile(BEProjectConfigureFilename):
        msg = 'Deleting old configure file [%s]' % \
              BEProjectConfigureFilename
        logger.debug(msg)
        remove(BEProjectConfigureFilename)
    
    msg = 'Adding the new configuration parameters to ' \
          'the configure file [%s]' % \
          BEProjectConfigureFilename
    logger.debug(msg)
    try:
        print args
        with open(BEProjectConfigureFilename, 'wb') as f:
            json.dump(args, f, indent=4, sort_keys=True)
    except Exception, e:
        msg = 'Unable to configure the build parameters; ' \
              'Reason [%s]' % e
        raise ConfigureFailed(msg)

    ConfigureSummary()
    return True


def ConfigureSummary():

    cfg_s  = '\n'
    cfg_s += 'The build system has been configured for ' \
             'the following paramaters:\n'
    cfg_s += '      Directories = [%s]\n' % ', '.join(CParams[Directories])
    cfg_s += '      Email       = [%s]\n' % ', '.join(CParams[Email])
    cfg_s += '      Package     = [%s]\n' % ', '.join(CParams[Package])
    cfg_s += '      Tag         = [%s]\n' % CParams[Tag]
    cfg_s += '      Verbose     = [%s]\n' % CParams[Verbose]
    cfg_s += '      Virtualenv  = [%s]\n' % CParams[Virtualenv]
    cfg_s += '      Timestamp   = [%s]\n' % datetime.now()
    cfg_s += 'You may now run (one-or-more of) the following targets:\n'
    cfg_s += '      -> dev\n'
    cfg_s += '      -> test\n'
    cfg_s += '      -> release\n'
    cfg_s += '      -> prelease\n'
    cfg_s += 'Goodluck with the build! ;) \n'
    print cfg_s
    logger.info(cfg_s)
    return None


def GetUserConfig(args):
    from be.dparams import DParams as UserConfig

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

    return UserConfig


# __END__
