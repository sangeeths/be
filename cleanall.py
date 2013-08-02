from be.clean import DoClean
from be.constants import BEProjectConfigureFilename
from be.util import GetLogger
from os import remove
from os.path import isfile


logger = GetLogger(__name__)


def DoCleanAll():

    DoClean()
    
    if isfile(BEProjectConfigureFilename):
        msg = 'Removing the configuring information [%s]' % \
              (BEProjectConfigureFilename)
        logger.debug(msg)
        remove(BEProjectConfigureFilename)

    msg = 'NOTE: Configure parameters has been removed; ' \
          'Please run \"be configure\" with sutiable ' \
          'parameters before attempting to build.\n'
    print msg
    logger.info(msg)

    return True

# __END__
