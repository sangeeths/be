
from be.constants import *

from be.exception import TargetCleanFailed
from be.exception import TargetConfigureFailed

from be.util import GetLogger
from be.util import GetLogger
from be.util import draw_line

from be.validation import valid_BEConfig
from be.validation import valid_CompileDirectory
from be.validation import valid_Email
from be.validation import valid_Package
from be.validation import valid_Tag
from be.validation import valid_VirtualEnvReqFile

from os import remove
from os import getcwd
from os import walk
from os.path import join
from os.path import normpath
from os.path import isfile
from os.path import isdir
from os.path import realpath

import fnmatch
import time
import json
import compileall

from subprocess import check_output


logger = GetLogger(__name__)


class BuildEngine:
    def __init__(self, args, config):
        self._target = args.target
        if self._target == Tconfigure:
            self._update_cparams(args)
        self._update_config(config)
        self._update_logger()
        self._op = {       
            Tclean     : self._clean,
            Tcleanall  : self._cleanall,
            Tconfigure : self._configure,
            Tdev       : self._dev,
            Ttest      : self._test,
            Trelease   : self._release,
            Tprelease  : self._prelease,
        }
        self._summary = ''
        self._dirs_ignored   = []
        self._dirs_compiled  = []
        self._files_ignored  = []
        self._files_compiled = []

    def _update_config(self, config):
        valid_BEConfig(config)
        for k, v in config.iteritems():
            setattr(self, '_%s' % k, v)
        self._update_dir_abspath()
        return None
        
    def _update_dir_abspath(self):
        _abspath = []
        for d in self._Directories:
            valid_CompileDirectory(d)
            _abspath.append(realpath(d))
        self._Directories = _abspath
        return None

    def _update_cparams(self, args):
        print args
        self._config_dirs       = args.dirs
        self._config_email      = args.email
        self._config_package    = args.package
        self._config_tag        = args.tag
        self._config_verbose    = args.verbose
        self._config_virtualenv = args.virtualenv
        return None

    def _update_logger(self):
        global logger
        if self._Verbose is True:
            logger = GetLogger(__name__, verbose=True)
            logger.debug('Verbose settings updated!')
        return None

    def _clean(self):
        CleanFiles = []
        try:
            Start = time.clock()
            for CurrentPath, LocalDirs, LocalFiles in walk('.'):
                for LocalFile in fnmatch.filter(LocalFiles, '*.pyc'):
                    CleanFile = join(CurrentPath, LocalFile)
                    CleanFiles.append(CleanFile)
                    remove(CleanFile)
            Stop = time.clock()
        except Exception, e:
            msg = 'Unable to clean the build directory; ' \
                  'Reason [%s]' % e
            raise TargetCleanFailed(msg)
        #
        # Update the summary (reset)
        self._summary = '\n'
        if CleanFiles:
            self._summary += 'The following files have been removed:\n'
            self._summary += '\t%s' % ('\n\t'.join(CleanFiles))
            self._summary += '\n'
        self._summary += '\nClean Time = %s Seconds\n' % (Stop-Start)
        self._summary += 'Total .pyc Files Removed = %d\n' % len(CleanFiles)
        logger.info(self._summary)
        return True

    def _cleanall(self):
        # Firstly, call clean()
        self._op[Tclean]()
        # Secondly, remove the configure information
        if isfile(BEProjectConfigureFilename):
            msg = 'Removing the configuring information [%s]' % \
                  (BEProjectConfigureFilename)
            logger.debug(msg)
            remove(BEProjectConfigureFilename)
        msg = '\nNOTE: Configure parameters has been removed; ' \
              'Please run \"be configure\" with sutiable ' \
              'parameters before attempting to build.\n'
        logger.info(msg)
        # Update the summary (append)
        self._summary += msg
        return True

    def _get_user_config(self):
        if self._config_dirs:
            self._Directories = self._config_dirs
            self._update_dir_abspath()
            logger.debug('Updating Directories..')
        if self._config_email:
            self._Email = [valid_Email(e) for e in self._config_email]
            logger.debug('Updating Emails..')
        if self._config_package:
            self._Package = [valid_Package(p) for p in self._config_package]
            logger.debug('Updating Packages..')
        if self._config_tag:
            self._Tag = valid_Tag(self._config_tag)
            logger.debug('Updating Tag..')
        if self._config_verbose is not None:
            self._Verbose = self._config_verbose
            logger.debug('Updating Verbose..')
        if self._config_virtualenv:
            if valid_VirtualEnvReqFile(self._config_virtualenv):
                self._Virtualenv = self._config_virtualenv
                logger.debug('Updating VirtualEnv..')

    def _get_config_params(self):
        config = {
            Directories : self._Directories,
            Email       : self._Email,
            Package     : self._Package,
            Tag         : self._Tag,
            Verbose     : self._Verbose,
            Virtualenv  : self._Virtualenv,
        }
        return config

    def _update_configure_summary(self):
        # Update the summary (reset)
        _s  = '\n'
        _s += 'The build system has been configured for ' \
                 'the following paramaters:\n'
        _s += '      Directories = [%s]\n' % ', '.join(self._Directories)
        _s += '      Email       = [%s]\n' % ', '.join(self._Email)
        _s += '      Package     = [%s]\n' % ', '.join(self._Package)
        _s += '      Tag         = [%s]\n' % self._Tag
        _s += '      Verbose     = [%s]\n' % self._Verbose
        _s += '      Virtualenv  = [%s]\n' % self._Virtualenv
        _s += '\nYou may now run (one-or-more of) the following targets:\n'
        _s += '      -> dev\n'
        _s += '      -> test\n'
        _s += '      -> release\n'
        _s += '      -> prelease\n'
        _s += 'Goodluck with the build! ;) \n'
        self._summary = _s
        logger.info(self._summary)
        return None
        
    def _configure(self):
        self._get_user_config()
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
            with open(BEProjectConfigureFilename, 'wb') as f:
                json.dump(self._get_config_params(), f, 
                          indent=4, sort_keys=True)
        except Exception, e:
            msg = 'Unable to configure the build parameters; ' \
                  'Reason [%s]' % e
            raise TargetConfigureFailed(msg)
        self._update_configure_summary()
        return True


    def _load_local_config(self, CurrentPath):
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

    def _build_dependency(self, CurrentPath, LocalBEConfig):
        if Dependency in LocalBEConfig and \
           LocalBEConfig[Dependency]:
            for target in LocalBEConfig[Dependency]:
                try:
                    logger.info('Running target %s' % target)
                    o = check_output(['make', '-C', CurrentPath, target])
                    logger.debug(o)
                except Exception, e:
                    msg = 'Compilation Failed for Target %s; ' \
                          'Reason [%s]' % (target, e)
                    print msg
                    logger.error(msg)
        return True

    def _update_files_ignored(self, CurrentPath, LocalBEConfig, LocalFiles):
        if LocalBEConfig != DefaultLocalBEConfig:
            # Check whether there is any configurations
            # to ignore any files in the current path,
            # if so ignore them!
            if IgnoreFileNames in LocalBEConfig and \
               LocalBEConfig[IgnoreFileNames]:
                for f in LocalBEConfig[IgnoreFileNames]:
                    try:
                        logger.debug('Ignoring %s' % f)
                        LocalFiles.remove(f)
                        #
                        # Update the self._files_ignored for statistics
                        _abspath = normpath(join(CurrentPath, f))
                        self._files_ignored.append(_abspath)
                    except Exception, e:
                        msg = '%s does not exist; Please fix \"%s\" ' \
                              'in %s; Reason [%s]' % (f, IgnoreFileNames, 
                              BEConfigFilename, e)
                        logger.error(msg)
        #
        # Ignore all files that are not Python files (.py)
        NonPythonFiles = [f for f in LocalFiles if not f.endswith('.py')]
        for f in NonPythonFiles: 
            msg = 'Ignoring Non Python File [%s]' % f
            logger.debug(msg)
            LocalFiles.remove(f)
            # Update the self._files_ignored for statistics
            _abspath = normpath(join(CurrentPath, f))
            self._files_ignored.append(_abspath)
        return LocalFiles

    def _compile_all(self, CurrentPath, CompileFiles):
        for f in CompileFiles:
            _f = normpath(join(CurrentPath, f))
            logger.debug('compiling %s' % _f)
            try:
                compileall.compile_file(_f, force=True, quiet=True)
            except Exception, e:
                msg = 'Compilation aborted for [%s]; Please ' \
                      'fix this issue and try again; ' \
                      'Reason[%s]' % (_f, e)
                logger.error(msg)
                return False
            # Update self._files_compiled for statistics
            self._files_compiled.append(_f)
        return True

    def _update_dirs_ignored(self, CurrentPath, LocalBEConfig):
        if IgnoreDirNames in LocalBEConfig and \
           LocalBEConfig[IgnoreDirNames]:
            for d in LocalBEConfig[IgnoreDirNames]:
                _abspath = normpath(join(CurrentPath, d))
                self._dirs_ignored.append(_abspath)
                msg = '%s is being ignored..' % _abspath
                logger.debug(msg)
        return None

    def _traverse_and_compile(self, RootDir):
        if not isdir(RootDir):
            msg = '%s is not a valid directory; Please ' \
                  'check your configuration' % (RootDir)
            logger.critical(msg)
            return False
        # Traverse!
        for CurrentPath, LocalDirs, LocalFiles in walk(RootDir):
            if CurrentPath in self._dirs_ignored:
                msg = 'As per the user config, %s is ' \
                      'being ignored!' % (CurrentPath)
                logger.info(msg)
                #DrawLine()
                continue
            #
            logger.debug("CurrentPath  : %s" % CurrentPath)
            logger.debug("LocalDirs    : %s" % LocalDirs)
            logger.debug("LocalFiles   : %s" % LocalFiles)
            #
            # Initialize the local config file
            # with the default config setting
            LocalBEConfig = DefaultLocalBEConfig
            #
            # If config file is present, then load it!
            if BEConfigFilename in LocalFiles:
                LocalBEConfig = self._load_local_config(CurrentPath)
            #
            # Firstly, build the dependency, if there is any!
            self._build_dependency(CurrentPath, LocalBEConfig)
            #
            # Update the locally ignored files to 
            # the self._files_ignored for statistics
            CompileFiles = self._update_files_ignored(CurrentPath,
                                                      LocalBEConfig,
                                                      LocalFiles)
            #
            # Compile rest of the files in the current path!
            if not self._compile_all(CurrentPath, CompileFiles):
                return False
            #
            # Add the local dir names that has
            # to be ignored to the global list
            self._update_dirs_ignored(CurrentPath, LocalBEConfig)
            logger.debug(draw_line())
            #
        return True

    def _dev(self):
        Start = time.clock()
        # NOTE: If self._Directories is empty then
        #       compile all directories else compile
        #       only the given directories!
        if not self._Directories:
            self._traverse_and_compile(getcwd())
        else:
            for CompileDir in self._Directories:
                self._traverse_and_compile(CompileDir)
        Stop = time.clock()
        #
        # Update the summary (reset)
        self._summary  = '\nTotal Compilation Time = %s ' \
                         'Seconds \n' % (Stop-Start)
        logger.info(self._summary)
        return None


        pass
    def _test(self):
        pass
    def _release(self):
        pass
    def _prelease(self):
        pass

    def run(self):
        op = self._op[self._target]
        op()

    def summary(self):
        if not self._Verbose:
            print self._summary


