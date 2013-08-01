import os
import time
from os.path import join, normpath
import json

start_time = time.time()

BEConfigFilename = 'config.be'

IgnoreDirNames  = 'IgnoreDirNames'
IgnoreFileNames = 'IgnoreFileNames'


DefaultLocalBEConfig = {IgnoreFileNames: [BEConfigFilename]}


def LoadLocalBEConfig(CurrentPath):
    LocalBEConfigFile = normpath(join(CurrentPath, BEConfigFilename))
    if not os.path.isfile(LocalBEConfigFile):
        print 'ERROR: %s not present' % LocalBEConfigFile
        return {}
    with open(LocalBEConfigFile, 'rb') as f:
        LocalBEConfig = json.load(f)
    print '%s contains the following config: \n %s' % \
          (BEConfigFilename, LocalBEConfig)
    return LocalBEConfig


def GetCompileFiles(LocalBEConfig, LocalFiles):

    if LocalBEConfig != DefaultLocalBEConfig:
        # Check whether there is any configurations 
        # to ignore any files in the current path, 
        # if so ignore them!
        if IgnoreFileNames in LocalBEConfig and \
           LocalBEConfig[IgnoreFileNames]:
            for localfile in LocalBEConfig[IgnoreFileNames]:
                try:
                    print 'INFO: ignoring %s' % localfile
                    LocalFiles.remove(localfile)
                except Exception, e:
                    print 'ERROR: %s not found; Reason [%s]' % (localfile, e)

    # Ignore all files that are not 
    # Python files (.py)
    NonPythonFiles = [f for f in LocalFiles if not f.endswith('.py')]
    if NonPythonFiles:
        for NonPythonFile in NonPythonFiles:
            print 'INFO: %s is not a Python file; Ignoring it!' % NonPythonFile
        
    PythonFiles = [f for f in LocalFiles if f.endswith('.py')]

    return PythonFiles
                

def DoCompile(LocalCompileFiles):
    for filename in LocalCompileFiles:
        print 'COMPILE: compiling %s' % filename
    return None


def GetIgnoreDirNames(CurrentPath, LocalBEConfig):
    
    LocalDirNames = []
    
    if IgnoreDirNames in LocalBEConfig and \
       LocalBEConfig[IgnoreDirNames]:
        for dirname in LocalBEConfig[IgnoreDirNames]:
            LocalDirNames.append(normpath(join(CurrentPath, dirname)))

    print 'INFO: the following local dir names are to be ignored : %s' % LocalDirNames
    return LocalDirNames



def TraverseAndCompile(root):

    if not os.path.isdir(root):
        print "%s does not seem to be a valid directory; Please check.." % root
        return None

    GlobalIgnoreDirNames = []
    for CurrentPath, LocalDirs, LocalFiles in os.walk(root):

        if CurrentPath in GlobalIgnoreDirNames:
            print 'INFO: IGNORE: %s is configured to be ignored; doing so.. ' % CurrentPath
            continue

        print "CurrentPath  : ", CurrentPath
        print "LocalDirs    : ", LocalDirs
        print "LocalFiles   : ", LocalFiles

        # Initialize the local config file
        # with the default config setting 
        LocalBEConfig = DefaultLocalBEConfig

        # If config file is present, then load it!
        if BEConfigFilename in LocalFiles:
            LocalBEConfig = LoadLocalBEConfig(CurrentPath)

        # TODO TODO TODO
        # Do 'make' here for the .c files
    
        LocalCompileFiles = GetCompileFiles(LocalBEConfig, LocalFiles)
        DoCompile(LocalCompileFiles)

        # Get the local dir names that has to ignored
        LocalIgnoreDirNames = GetIgnoreDirNames(CurrentPath, LocalBEConfig)

        # Add the local dir names that has 
        # to be ignored to the global list
        for dirname in LocalIgnoreDirNames:
            GlobalIgnoreDirNames.append(dirname)

        print '----------------------------------'
 


TraverseAndCompile('/home/sangeeth/trials/build/dir1')


print 'Total time taken = ', time.time() - start_time, "seconds"


