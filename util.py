

def GetLogger(LoggerName, verbose=False):
    from be.config import BELogFormat
    from be.config import BELogLevel
    from be.config import BELogFileName
    import logging
    import sys

    # Create a logger
    logger = logging.getLogger(LoggerName)
    logger.setLevel(BELogLevel)

    # Create a formatter
    formatter = logging.Formatter(BELogFormat)

    # verbose = StreamHandler
    if verbose:
        # Create a stream handler; Set a loglevel; 
        # Set a formatter; Add the stream handler
        # to the logger
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(BELogLevel)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger

    # Create a file handler; Set a loglevel; 
    # Set a formatter; Add the file handler
    # to the logger
    file_handler = logging.FileHandler(BELogFileName)
    file_handler.setLevel(BELogLevel)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def DrawLine(style='-'):
#    import os
#    rows, columns = os.popen('stty size', 'r').read().split()
    return style * 50


def GetProjectDefaultParameters():
    from be.constants import BEProjectDefaultConfigFilename as ProjDefaultCfg
    from be.exception import GetProjectDefaultConfigFailed
    from os.path import realpath, isfile
    import json
    logger = GetLogger(__name__)
    AbsPathPrjDefCfgFile = realpath(ProjDefaultCfg)
    if not isfile(AbsPathPrjDefCfgFile):
        msg = 'The default config file [%s] does not exist or ' \
              'does not seem to be valid. Please save your ' \
              'project build preference to [%s] file.' % \
              (ProjDefaultCfg, AbsPathPrjDefCfgFile)
        logger.error(msg)
        raise GetProjectDefaultConfigFailed(msg)
    try:
        with open(ProjDefaultCfg, 'rb') as f:
            ProjectDefaultParameters = json.load(f)
    except Exception, e:
        msg = 'Unable to read the default configurations from ' \
              '[%s] file; Please (re-)check the format in which ' \
              'the configurations are stored; Reason [%s]' % \
              (AbsPathPrjDefCfgFile, e)
        logger.error(msg)
        raise GetProjectDefaultConfigFailed(msg)
    return ProjectDefaultParameters


def GetProjectConfigureParameters():
    from be.constants import BEProjectConfigureFilename as CfgFile
    from be.exception import GetProjectConfigureParametersFailed
    from os.path import realpath, isfile
    import json
    logger = GetLogger(__name__)
    AbsPathCfgFile = realpath(CfgFile)
    msg = 'The configure information [%s] does not exist or ' \
          'does not seem to be valid. From your project root ' \
          'directory please (re-)run \"be configure\" with the ' \
          'sutiable parameters' % (AbsPathCfgFile)
    if not isfile(AbsPathCfgFile):
        logger.error(msg)
        raise GetProjectConfigureParametersFailed(msg)
    try:
        with open(AbsPathCfgFile, 'rb') as f:
            ProjectConfigureParameters = json.load(f)
    except Exception, e:
        msg += '; Reason[%s] ' % e
        logger.error(msg)
        raise GetProjectConfigureParametersFailed(msg)
    return ProjectConfigureParameters



