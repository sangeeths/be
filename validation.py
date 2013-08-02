from be.constants import BEPackageType

from be.default import BEProjectRootDirectory

from be.exception import InvalidRootDirectory
from be.exception import InvalidEmailID 
from be.exception import InvalidPackage
from be.exception import InvalidTag

from be.util import GetLogger

import os


logger = GetLogger(__name__)


def ValidCompileDirectory(child):
    from be.exception import InvalidCompileDirectory
    from os import getcwd
    from os.path import realpath, isdir, commonprefix
    child  = realpath(child)
    parent = getcwd()
    if not isdir(child):
        msg = 'Invalid directory; Cannot compile [%s] as it ' \
              'does not look like a directory. Please fix the ' \
              'argument(s) for \"--dirs\" option.' % child
        logger.error(msg)
        raise InvalidCompileDirectory(msg)
    if not commonprefix([parent, child]) == parent:
        msg = 'Invalid directory settings; Cannot compile ' \
              'directory [%s] because it is not inside the ' \
              'project root directory [%s]; Please fix the ' \
              'argument(s) for \"--dirs\" option.' % (child, parent)
        logger.error(msg)
        raise InvalidCompileDirectory(msg)
    return True


def GetAbsPath(dirs):
    from os.path import realpath
    AbsPath = []
    for path in dirs:
        ValidCompileDirectory(path)
        AbsPath.append(realpath(path))
    return AbsPath
           

    

def ValidEmail(email):
    ValidEmailIds = [
        'all@riptideio.com',
        'andy@riptideio.com',
        'bhagavan@riptideio.com',
        'dleimbro@riptideio.com',
        'mark@riptideio.com',
        'mfranco@riptideio.com',
        'mogram@riptideio.com',
        'sangeeth@riptideio.com',
        'sleimbro@riptideio.com']
    if not email in ValidEmailIds:
        msg = 'Invalid Email Address [%s]; The valid options ' \
              'are one or more of %s' % (email, ValidEmailIds)
        logger.error(msg)
        raise InvalidEmailID(msg)
    return True


def GetEmails(emails):
    Emails = []
    for e in emails:
        if ValidEmail(e): Emails.append(e)
    return Emails


def PackageEnum(s):
    from be.constants import BEPackageType
    from be.util import StringToEnum
    try:
        return StringToEnum(BEPackageType, s)
    except Exception, e:
        msg = 'Invalid package type [%s]; The valid ' \
              'options are one or more of [%s]' % \
              (s, ', '.join(BEPackageType._keys))
        raise InvalidPackage(msg)
    return True


def GetPackages(packages):
    Packages = []
    for p in packages:
        Packages.append(PackageEnum(p))
    return Packages


def ValidTag(tag):
    from string import ascii_lowercase as lower
    from string import ascii_uppercase as upper
    from string import digits as digits
    
    _allowed = set(lower + digits + upper + '_' + '-')
    _min_len = 5
    _max_len = 50

    if tag is None: 
        msg = 'Invalid tag; Incoming \'None\' value'
        logger.error(msg)
        raise InvalidTag(msg)

    _entered = set(tag)
    not_allowed = _entered.difference(_allowed)
    if not_allowed:
        msg = 'Invalid character(s) found in tag [%s]; ' \
              'Invalid %s' % (tag, list(not_allowed))
        logger.error(msg)
        raise InvalidTag(msg)

    # _min_len <= len(tag) <= _max_len
    strlen = len(tag)
    if strlen >= _min_len and strlen <= _max_len:
        return True

    msg = 'Invalid String Length (%s) [%d]; min_len [%d]; ' \
          'max_len [%d]' % (tag, strlen, _min_len, _max_len)
    logger.error(msg)
    raise InvalidTag(msg)


def ValidVirtualEnvReqFile(ReqFile):
    from os.path import realpath, isfile
    ReqFile = realpath(ReqFile)
    if not isfile(ReqFile):
        msg = 'Invalid Requirement File for VirtualEnv [%s]; ' \
              'Please update your option for \"--virtualenv\" '\
              'in \"be configure\" command.' % (ReqFile)
        raise InvalidVirtualEnvReqFile(msg)
    return True


