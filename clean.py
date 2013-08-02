from be.exception import CleanFailed
from be.util import GetLogger
from datetime import datetime
import fnmatch
import os

logger = GetLogger(__name__)


def DoClean():
    clean = []
    try:
        for root, dirnames, filenames in os.walk('.'):
            for filename in fnmatch.filter(filenames, '*.pyc'):
                f = os.path.join(root, filename)
                clean.append(f)
                os.remove(f)
    except Exception, e:
        msg = 'Unable to clean the build directory; ' \
              'Reason [%s]' % e
        raise CleanFailed(msg)

    clean_s = '\n'
    if clean:
        clean_s += 'The following files have been removed:\n'
        for f in clean:
            clean_s += '    %s\n' % f
    clean_s += 'Timestamp = [%s]\n' % datetime.now()
    clean_s += 'Total pyc Files Removed = [%d]\n' % len(clean)

    print clean_s
    logger.info(clean)

    return True

