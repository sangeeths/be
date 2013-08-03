
from be.constants import *
from be.config import *

from be.exception import TargetCleanFailed
from be.exception import TargetConfigureFailed
from be.exception import GenerateTgzFailed
from be.exception import GenerateMD5SumFailed
from be.exception import UnableToAddPackageFiles
from be.exception import UnableToIgnoreItem

from be.util import GetLogger
from be.util import GetLogger
from be.util import DrawLine

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
from os.path import basename

import re
import fnmatch
import time
import json
import compileall
import tarfile
import hashlib

from subprocess import check_output

from datetime import datetime

logger = GetLogger(__name__)




class BuildEngine:
    def __init__(self, args, config):
        self._target = args.target
        if self._target == Tconfigure:
            self._update_cparams(args)
        self._update_config(config)
        self._update_logger()
        self._target_op = {       
            Tclean     : self._clean,
            Tcleanall  : self._cleanall,
            Tconfigure : self._configure,
            Tdev       : self._dev,
            Ttest      : self._test,
            Trelease   : self._release,
            Tprelease  : self._prelease,
        }
        self._package_op = {
            Tgz : self._tgz,
            Rpm : self._rpm,
        }
        self._summary = ''
        self._update_filenames()
        self._dirs_ignored   = []
        self._dirs_compiled  = []
        self._files_ignored  = []
        self._files_compiled = []
        self._add_to_pkg     = []

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
        self._config_dirs       = args.dirs if args.dirs is not None else []
        self._config_email      = args.email if args.email is not None else []
        self._config_package    = args.package if args.package is not None else []
        self._config_tag        = args.tag if args.tag is not None else ''
        self._config_verbose    = args.verbose
        self._config_virtualenv = args.virtualenv if args.virtualenv is not None else ''
        # The following will remove duplicates
        self._config_dirs    = list(set(self._config_dirs))
        self._config_email   = list(set(self._config_email))
        self._config_package = list(set(self._config_package))
        return None

    def _update_logger(self):
        global logger
        if self._Verbose is True:
            logger = GetLogger(__name__, verbose=True)
            logger.debug('Verbose settings updated!')
        return None

    def _update_filenames(self):
        # The .tgz and .rpm file names are required only
        # for the build targets like dev, test, release 
        # and prelease; This function is applicable for
        # only the build targets!
        if not self._build_target():
            return None

        # Add basename and target
        f = '%s-%s' % (BEBaseFileName, self._target)
        # Add tag
        if self._Tag: 
            f += '-%s' % self._Tag
        # TODO TODO
        # Add version information here!
        # Add timestamp
        if self._target == Tdev or self._target == Ttest:
            ts = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        else:
            ts = datetime.now().strftime('%Y-%m-%d')
        f += '-%s' % ts 
        fname = normpath(join(BEOutputDirectory, f))
        self._tgz_filename = '%s.%s' % (fname, Tgz)
        self._rpm_filename = '%s.%s' % (fname, Rpm)
        return None

    def _build_target(self):
        if self._target == Tdev or \
           self._target == Ttest or \
           self._target == Trelease or \
           self._target == Tprelease:
            return True
        return False
    
    def _get_package_files(self, rootdir):
        # This list contains all the files that should be tar'ed
        _pkg_files = []
        for CurrentPath, LocalDirs, LocalFiles in walk(rootdir):
            for name in LocalFiles:
                f = normpath(join(CurrentPath, name))
                if f.endswith('.pyc'):
                    _pkg_files.append(f)
                if f in self._add_to_pkg:
                    _pkg_files.append(f)
        return _pkg_files

    # # # # # # # # # # # # # #    C L E A N    # # # # # # # # # # # # # # 

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
            self._summary += '\n\n'
        self._summary += 'Total Number of .pyc Files Removed = %d\n' % len(CleanFiles)
        self._summary += 'Clean Time = %s Seconds\n' % (Stop-Start)
        #logger.info(self._summary)
        return True

    # # # # # # # # # # # #    C L E A N - A L L   # # # # # # # # # # # #

    def _cleanall(self):
        # Firstly, call clean()
        self._target_op[Tclean]()
        # Secondly, remove the configure information
        if isfile(BEProjectConfigureFilename):
            msg = 'Removing the configuring information [%s]' % \
                  (BEProjectConfigureFilename)
            logger.debug(msg)
            remove(BEProjectConfigureFilename)
        msg = '\nNOTE: Configure parameters has been removed; ' \
              'Please run \"be configure\" with sutiable ' \
              'parameters before attempting to build.\n'
        #logger.info(msg)
        # Update the summary (append)
        self._summary += msg
        return True

    # # # # # # # # # # # #    C O N F I G U R E   # # # # # # # # # # # #

    def _get_user_config(self):
        # Update Directories
        self._Directories = self._config_dirs
        self._update_dir_abspath()
        logger.debug('Updating Directories..')
        # Update Emails
        self._Email = [valid_Email(e) for e in self._config_email]
        logger.debug('Updating Emails..')
        # Update Package
        self._Package = [valid_Package(p) for p in self._config_package]
        logger.debug('Updating Packages..')
        # Update Tag
        self._Tag = valid_Tag(self._config_tag)
        logger.debug('Updating Tag..')
        # Update Verbose
        if self._config_verbose is not None:
            self._Verbose = self._config_verbose
            logger.debug('Updating Verbose..')
        # Update Virtual Env
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
        _s += '      Directories = %s\n' % self._Directories
        _s += '      Email       = %s\n' % self._Email
        _s += '      Package     = %s\n' % self._Package
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
        #logger.info(self._summary)
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
            msg = 'Updating configure parameters : ' \
                  '%s' % self._get_config_params()
            logger.debug(msg)
        except Exception, e:
            msg = 'Unable to configure the build parameters; ' \
                  'Reason [%s]' % e
            raise TargetConfigureFailed(msg)
        self._update_configure_summary()
        return True

    # # # # # # # # # # # # # #    D E V    # # # # # # # # # # # # # # #

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
        msg = '%s contains: %s' % (BEConfigFilename, LocalBEConfig)
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
    
    def _add_dir_to_package(self, dirname):
        if not isdir(dirname):
            return False
        for path, dirs, files in walk(dirname):
            for f in files:
                logger.debug('Adding [D] File: %s' % f)
                _f = normpath(join(path, f))
                self._add_to_pkg.append(_f)
        return True

    def _add_to_package(self, CurrentPath, LocalBEConfig, 
                        LocalDirs, LocalFiles):
        # If there is no "AddToPackage" in LocalBEConfig
        # or if LocalBEConfig[AddToPackage] is empty, then
        # there is nothing to add.. so just leave right now!
        if AddToPackage not in LocalBEConfig:
            return None
        if not LocalBEConfig[AddToPackage]:
            return None
        # Now, for all the files and directories present 
        # in "AddToPackage", add them to self._add_to_pkg
        for f in LocalBEConfig[AddToPackage]:
            try:
                regex = re.compile(f)
                AddFiles = [x for x in LocalFiles if regex.search(x)]
                for f in AddFiles:
                    logger.debug('Adding File: %s' % f)
                    _f = normpath(join(CurrentPath, f))
                    self._add_to_pkg.append(_f)
                AddDirs = [x for x in LocalDirs if regex.search(x)]
                for d in AddDirs:
                    logger.debug('Adding Directory: %s' % d)
                    _d = normpath(join(CurrentPath, d))
                    self._add_dir_to_package(_d)
            except Exception, e:
                msg = 'Unable to add %s to the Package; Please fix \"%s\" ' \
                      'in %s; Reason [%s]' % (f, AddToPackage, 
                      BEConfigFilename, e)
                logger.error(msg)
                raise UnableToAddPackageFiles(msg)
        return True

    def _add_dir_to_ignore_items(self, dirname):
        if not isdir(dirname):
            return False
        self._dirs_ignored.append(dirname)
        for path, dirs, files in walk(dirname):
            for f in files:
                _f = normpath(join(path, f))
                logger.debug('Ignore [D] File: %s' % f)
                self._files_ignored.append(_f)
            for d in dirs:
                _d = normpath(join(path, d))
                logger.debug('Ignore [D] Directory: %s' % d)
                self._dirs_ignored.append(_d)
        return True

    def _update_ignore_items(self, CurrentPath, LocalBEConfig, 
                             LocalDirs, LocalFiles):
        for item in LocalBEConfig[IgnoreItems]:
            try:
                regex = re.compile(item)
                IgnoreFiles = [x for x in LocalFiles if regex.search(x)]
                for f in IgnoreFiles:
                    logger.debug('Ignoring File: %s' % f)
                    LocalFiles.remove(f)
                    #
                    # Update the self._files_ignored for statistics
                    _f = normpath(join(CurrentPath, f))
                    self._files_ignored.append(_f)
                IgnoreDirs = [x for x in LocalDirs if regex.search(x)]
                for d in IgnoreDirs:
                    logger.debug('Ignoring Directroy: %s' % d)
                    # Update the self._dirs_ignored for statistics
                    _d = normpath(join(CurrentPath, d))
                    self._add_dir_to_ignore_items(_d)
            except Exception, e:
                msg = '%s does not exist; Please fix \"%s\" ' \
                      'in %s; Reason [%s]' % (f, IgnoreItems, 
                      BEConfigFilename, e)
                logger.error(msg)
                raise UnableToIgnoreItem(msg)
        #
        # Ignore all files that are not Python files (.py)
        NonPythonFiles = [f for f in LocalFiles if not f.endswith('.py')]
        for f in NonPythonFiles: 
            msg = 'Ignoring Non Python File: [%s]' % f
            logger.debug(msg)
            LocalFiles.remove(f)
            # Update the self._files_ignored for statistics
            _abspath = normpath(join(CurrentPath, f))
            self._files_ignored.append(_abspath)
        return LocalFiles

    def _compile_all(self, CurrentPath, CompileFiles):
        for f in CompileFiles:
            _f = normpath(join(CurrentPath, f))
            if not self._Verbose:
                print 'compiling %s' % _f
            else:
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

    def _traverse_and_compile(self, RootDir):
        if not isdir(RootDir):
            msg = '%s is not a valid directory; Please ' \
                  'check your configuration' % (RootDir)
            logger.critical(msg)
            return False
        # Traverse!
        for CurrentPath, LocalDirs, LocalFiles in walk(RootDir):
            if CurrentPath in self._dirs_ignored:
                logger.info('Ignoring Directroy: %s' % CurrentPath)
                logger.debug(DrawLine())
                continue
            #
            # Update the self._dirs_compiled
            # with the CurrentPath
            self._dirs_compiled.append(CurrentPath)
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
            # Update self._add_to_package and add all the 
            # files and directories that should be added 
            # to the package
            self._add_to_package(CurrentPath, 
                                 LocalBEConfig, 
                                 LocalDirs, 
                                 LocalFiles)
            #
            # Update the locally ignored files to 
            # the self._files_ignored for statistics
            CompileFiles = self._update_ignore_items(CurrentPath,
                                                     LocalBEConfig,
                                                     LocalDirs, 
                                                     LocalFiles)
            #
            # Compile rest of the files in the current path!
            if not self._compile_all(CurrentPath, CompileFiles):
                return False
            logger.debug(DrawLine())
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
        _s  = '\n'
        _s += 'Build Summary:\n'
        _s += '--------------\n'
        _s += 'Total Number of Files Compiled = %d\n' % len(self._files_compiled)
        _s += 'Total Number of Files Ignored  = %d\n' % len(self._files_ignored)
        _s += 'Total Number of Dirs Compiled  = %d\n' % len(self._dirs_compiled)
        _s += 'Total Number of Dirs Ignored   = %d\n' % len(self._dirs_ignored)
        _s += '\nTotal Compilation Time = %s Seconds \n' % (Stop-Start)
        self._summary = _s
        #logger.info(self._summary)

        _s  = 'Compiled Files:\n%s\n' % self._files_compiled
        _s += 'Ignored Files:\n%s\n' % self._files_ignored
        _s += 'Compiled Directories:\n%s\n' % self._dirs_compiled
        _s += 'Ignored Directories:\n%s\n' % self._dirs_ignored
        _s += 'Add to Package:\n%s\n' % self._add_to_pkg
        logger.debug(_s)
        return None

    # # # # # # # # # # # # # #    T E S T   # # # # # # # # # # # # # # #

    def _test(self):
        pass

    # # # # # # # # # # # #    R E A L E S E    # # # # # # # # # # # # # 

    def _release(self):
        pass

    # # # # # # #    P R O D U C T I O N - R E A L E S E    # # # # # # #

    def _prelease(self):
        pass

    
    # # # # # # # # # # # # # #    T G Z    # # # # # # # # # # # # # # #

    def _tgz(self):
        rootdir = getcwd()
        _tgz_files = self._get_package_files(rootdir)
        # Generate tzg!
        try:
            with tarfile.open(self._tgz_filename, "w:gz") as tar:
                for f in _tgz_files:
                    tardir = normpath(f.replace(rootdir, BETargetRoot))
                    tar.add(f, recursive=False, arcname=tardir)
        except Exception, e:
            msg = 'Unable to generate tgz file [%s]; ' \
                  'Reason [%s]' % (f, e)
            raise GenerateTgzFailed(msg)
        # Generate MD5Sum for the tarfile
        self._summary += '\nTgz : %s\n' % (self._tgz_filename)
        self._generate_md5sum(self._tgz_filename)
        return None

    # # # # # # # # # # # # # #    R P M    # # # # # # # # # # # # # # #

    def _rpm(self):
#        # Step-1 : Create the RPM build environment
#        # mkdir -p rpmbuild/{RPMS,SRPMS,BUILD,SOURCES,SPECS,tmp}
#        logger.debug('Clearing existing rpmbuild setup!')
#        o = check_output(['rm', '-rf', BERPMBuildDir])
#        logger.debug(o)
#
#        logger.debug('Creating rpmbuild build environment [%s]' % dirname)
#        dirname = '%s/%s' % (BERPMBuildDir, '{RPMS,SRPMS,BUILD,SOURCES,SPECS,tmp}')
#        o = check_output(['mkdir', '-p', dirname])
#        logger.debug(o)
#
#        
#        # Step-2 : Create the tgz file
        pass


    # # # # # # # # # # # # #   E - M A I L   # # # # # # # # # # # # # #
    
    def _send_email(self):
        pass

    # # # # # # # # # # # # #   M D 5 S U M   # # # # # # # # # # # # # #

    def _generate_md5sum(self, fname):
        try:
            md5sum = hashlib.md5(open(fname, 'rb').read()).hexdigest()
            content = '%s %s\n' % (md5sum, basename(fname))
            md5file = '%s.md5' % (fname)
            with open(md5file, 'w') as f:
                f.write(content)
        except Exception, e:
            msg = 'Unable to Generate md5sum for %s; ' \
                  'Reason [%s]' % (fname, e)
            raise GenerateMD5SumFailed(msg)
        self._summary += '    : %s\n' % (md5file)
        return True


    def run(self):
        target_op = self._target_op[self._target]
        target_op()

        # If the target is dev, test, release, prelease
        # then generate the packages (tgz and/or rpm)
        if self._build_target():
            for p in self._Package:
                package_op = self._package_op[p]
                package_op()

    def summary(self):
        # NOTE: When existing verbose is False and 
        #       new verbose is True [corner-case]
        if self._target == Tconfigure and \
           self._config_verbose == True:
            print self._summary
            logger.debug(self._summary)
            return None

        if not self._Verbose:
            print self._summary
        else:
            logger.debug(self._summary)


# __END__
