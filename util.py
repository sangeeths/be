

def GetLogger(LoggerName):
    from be.constants import BELogFormat
    from be.constants import BELogLevel
    from be.default import BELogFileName
    from be.default import BEVerbose
    import logging
    import sys

    # Create a logger
    logger = logging.getLogger(LoggerName)
    logger.setLevel(BELogLevel)

    # Create a formatter
    formatter = logging.Formatter(BELogFormat)

    # Create a file handler; Set a loglevel; 
    # Set a formatter; Add the file handler
    # to the logger
    file_handler = logging.FileHandler(BELogFileName)
    file_handler.setLevel(BELogLevel)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Iff verbose mode 
    # Create a stream handler; Set a loglevel; 
    # Set a formatter; Add the stream handler
    # to the logger
    if BEVerbose:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(BELogLevel)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger

def draw_line(style='-'):
#    import os
#    rows, columns = os.popen('stty size', 'r').read().split()
    return style * 50

def DrawLine():
    logger = GetLogger(__name__)
    line = '-' * 50
    logger.info(line)
    return None




    

