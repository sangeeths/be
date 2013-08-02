from be.constants import BEPackageType

from be.default import BEProjectRootDirectory

from be.exception import InvalidDirectory
from be.exception import InvalidEmailID 
from be.exception import InvalidPackage
from be.exception import InvalidTag

from be.util import GetLogger

import os


logger = GetLogger(__name__)


def ValidDirs(dirs):
    parent = os.path.realpath(BEProjectRootDirectory)
    for child in dirs:
        if not os.path.isdir(child):
            msg = 'Invalid directory; Cannot compile [%s] as it ' \
                  'does not look like a directory. Please fix the ' \
                  'argument(s) for \"--dirs\" option.' % child
            logger.error(msg)
            raise InvalidDirectory(msg)
        child = os.path.realpath(child)
        if not os.path.commonprefix([parent, child]) == parent:
            msg = 'Invalid directory settings; Cannot compile ' \
                  'directory [%s] because it is not inside the ' \
                  'project root directory [%s]; Please fix the ' \
                  'argument(s) for \"--dirs\" option.' % (child, parent)
            logger.error(msg)
            raise InvalidDirectory(msg)
    return True
    

def ValidEmail(emails):
    valid_email_ids = [
        'all@riptideio.com',
        'andy@riptideio.com',
        'bhagavan@riptideio.com',
        'dleimbro@riptideio.com',
        'mark@riptideio.com',
        'mfranco@riptideio.com',
        'mogram@riptideio.com',
        'sangeeth@riptideio.com',
        'sleimbro@riptideio.com']
    for email in emails:
        if not email in valid_email_ids:
            msg = 'Invalid Email Address [%s]; The valid options ' \
                  'are one or more of %s' % (email, valid_email_ids)
            logger.error(msg)
            raise InvalidEmailID(msg)
    return True


def ValidPackage(package):
    for p in package:
        if p not in BEPackageType._keys:
            msg = 'Invalid package type [%s]; The valid ' \
                  'options are one or more of [%s]' % \
                  (p, ', '.join(BEPackageType._keys))
            logger.error(msg)
            raise InvalidPackage(msg)
    return True


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


def ValidConfigureArguments(args):
    if args.dirs:
        ValidDirs(args.dirs)
    if args.email:
        ValidEmail(args.email)
    if args.package:
        ValidPackage(args.package)
    if args.tag:
        ValidTag(args.tag)
    return True


