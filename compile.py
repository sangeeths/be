from be.constants import BEConfigFilename
from be.util import GetLogger
from be.util import draw_line

from os import getcwd
from os import walk
from os.path import isdir
from os.path import isfile
from os.path import join
from os.path import normpath

import json

from datetime import datetime

logger = None


def LoadLocalBEConfig(CurrentPath):
    LocalBEConfigFile = normpath(join(CurrentPath, BEConfigFilename))
    if not isfile(LocalBEConfigFile):
        msg = 'Attempting to load the local configuration ' \
              '[%s] from %s; But the %s file is not present!' % \
              (BEConfigFilename, CurrentPath, LocalBEConfigFile)
        logger.error(msg)
        return {}
    with open(LocalBEConfigFile, 'rb') as f:
        LocalBEConfig = json.load(f)
    msg = '%s contains:\n\t%s' % \
          (BEConfigFilename, LocalBEConfig)
    logger.debug(msg)
    return LocalBEConfig


def GetCompileFiles(CurrentPath, LocalBEConfig, LocalFiles):
    from be.constants import DefaultLocalBEConfig
    from be.constants import IgnoreFileNames
    CompileFiles = []
    if LocalBEConfig != DefaultLocalBEConfig:
        # Check whether there is any configurations 
        # to ignore any files in the current path, 
        # if so ignore them!
        if IgnoreFileNames in LocalBEConfig and \
           LocalBEConfig[IgnoreFileNames]:
            for localfile in LocalBEConfig[IgnoreFileNames]:
                try:
                    logger.debug('Ignoring %s' % localfile)
                    LocalFiles.remove(localfile)
                except Exception, e:
                    msg = '%s does not exist; Please fix \"%s\" ' \
                          'in %s; Reason [%s]' % (localfile, 
                          IgnoreFileNames, BEConfigFilename, e)
                    logger.warning(msg)
    #
    # Ignore all files that are not Python files (.py)
    NonPythonFiles = \
        [f for f in LocalFiles if not f.endswith('.py')]
    if NonPythonFiles:
        msg = 'Ignoring [%s] as they are not Python files!' % \
              ', '.join(NonPythonFiles)
        logger.info(msg)
    #
    # Get all the Python files and convert them to 
    # fullpath; And, later return them!
    PythonFiles = [f for f in LocalFiles if f.endswith('.py')]
    if PythonFiles:
        for PythonFile in PythonFiles:
            CompileFiles.append(normpath(join(CurrentPath, PythonFile)))
    return CompileFiles
                

def CompileAll(LocalCompileFiles):
    import compileall
    for CompileFile in LocalCompileFiles:
        logger.debug('compiling %s' % CompileFile)
        try:
            compileall.compile_file(CompileFile, 
                                    force=True, 
                                    quiet=True)
        except Exception, e:
            msg = 'Compilation aborted; Please ' \
                  'fix this issue and try again; ' \
                  'Reason[%s]' % e
            logger.error(msg)
            return False
    return True


def GetIgnoreDirNames(CurrentPath, LocalBEConfig):
    from be.constants import IgnoreDirNames
    LocalDirNames = []
    if IgnoreDirNames in LocalBEConfig and \
       LocalBEConfig[IgnoreDirNames]:
        for dirname in LocalBEConfig[IgnoreDirNames]:
            LocalDirNames.append(normpath(join(CurrentPath, dirname)))
    msg = 'The following directory names will ' \
          'be ignored : %s' % LocalDirNames
    logger.info(msg)
    return LocalDirNames


def BuildDependency(CurrentPath, LocalBEConfig):
    from subprocess import check_output
    from be.constants import Dependency
    if Dependency in LocalBEConfig and \
       LocalBEConfig[Dependency]:
        for dependency in LocalBEConfig[Dependency]:
            try:
                logger.info('Running target %s' % dependency)
                logger.info(check_output(['make', '-C', CurrentPath, dependency]))
            except Exception, e:
                msg = 'Compilation Failed for Target %s; ' \
                      'Reason [%s]' % (dependency, e)
                logger.error(msg)
    return True



def TraverseAndCompile(RootDir):
    from be.constants import DefaultLocalBEConfig

    if not isdir(RootDir):
        msg = '%s is not a valid directory; Please ' \
              'check your configuration' % (RootDir)
        logger.critical(msg)
        return False

    # The list of directories that should be ignored
    GlobalIgnoreDirNames = []

    for CurrentPath, LocalDirs, LocalFiles in walk(RootDir):

        if CurrentPath in GlobalIgnoreDirNames:
            msg = 'As per the user config, %s is ' \
                  'being ignored!' % (CurrentPath)
            logger.info(msg)
            #DrawLine()
            continue

        logger.debug("CurrentPath  : %s" % CurrentPath)
        logger.debug("LocalDirs    : %s" % LocalDirs)
        logger.debug("LocalFiles   : %s" % LocalFiles)

        # Initialize the local config file
        # with the default config setting 
        LocalBEConfig = DefaultLocalBEConfig

        # If config file is present, then load it!
        if BEConfigFilename in LocalFiles:
            LocalBEConfig = LoadLocalBEConfig(CurrentPath)

        # Firstly, build the dependency, if there is any!
        BuildDependency(CurrentPath, LocalBEConfig)

        # TODO TODO TODO
        # Do 'make' here for the .c files
    
        LocalCompileFiles = GetCompileFiles(CurrentPath, 
                                            LocalBEConfig, 
                                            LocalFiles)
        if not CompileAll(LocalCompileFiles):
            return False

        # Get the local dir names that has to ignored
        LocalIgnoreDirNames = GetIgnoreDirNames(CurrentPath, 
                                                LocalBEConfig)

        # Add the local dir names that has 
        # to be ignored to the global list
        for dirname in LocalIgnoreDirNames:
            GlobalIgnoreDirNames.append(dirname)

        #DrawLine()
        #logger.debug('-' * 50)
        logger.debug(draw_line())

    return True


def DoCompile():
    from be.cparams import CParams
    from be.constants import Directories
    from be.constants import Verbose
    import time
    
    global logger
    
    _verbose = True if CParams[Verbose] else False
    logger = GetLogger(__name__, verbose=_verbose)
 
    # Start time  
    Start = time.clock()

    if not CParams[Directories]:
        TraverseAndCompile(getcwd())
    else:
        for CompileDir in CParams[Directories]:
            TraverseAndCompile(CompileDir)

    # Stop time  
    Stop = time.clock()

    msg = 'Total Compilation Time = %s Seconds' % (Stop-Start)
    print msg

    return True


# __END__
