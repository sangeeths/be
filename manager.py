from be.constants import *
from be.exception import ConfigureParametersNotFound
from be.util import GetLogger


logger = GetLogger(__name__)


_default_config = {
    Directories : [],
    Email       : [],
    Package     : [],
    Tag         : '',
    Verbose     : False,
    Virtualenv  : ''
}

class BEConfigManager:
    def __init__(self, args):
        self._config = None
        self._default = False
        self._target  = args.target
        self.configure()
        self.validConfig()

    def configure(self):
        try:
            from be.cparams import CParams
            self._config = CParams
            msg = 'Loading Configure Parameters; %s' % self._config
            logger.debug(msg)
        except Exception, e:
            msg = 'Unable to load Configuration ' \
                  'Parameters; Reason [%s]' % e
            logger.error(msg)
            # Load the default configuration!
            self._config = _default_config
            msg = 'Loading Default Configuration; %s' % self._config
            logger.info(msg)
            self._default = True
        return None   
    
    def validConfig(self):
        # NOTE: It is not possible to run 'dev', 'test', 
        #       'release', 'prelease' commands without
        #       running "be configure"
        if (self._target == Tdev       or \
            self._target == Ttest      or \
            self._target == Trelease   or \
            self._target == Tprelease) and \
            self._default == True:
            msg = 'Please run \"be configure\" with ' \
                  'sutiable parameters before attempting '\
                  'to %s' % (self._target)
            raise ConfigureParametersNotFound(msg)
        return True

    def getConfig(self):
        return self._config
        
