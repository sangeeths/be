from be.constants import Tdev
from be.constants import Tprelease
from be.constants import Trelease
from be.constants import Ttest
from be.exception import ConfigureParametersNotFound
from be.util import GetLogger


logger = GetLogger(__name__)


class BEConfigManager:
    def __init__(self, args):
        self._config = None
        self._cparams = False
        self._dparams = False
        self._target  = args.target
        self.configure()
        self.validConfig()

    def configure(self):
        try:
            from be.cparams import CParams
            self._config = CParams
            self._cparams = True
        except Exception, e:
            msg = 'Unable to load Configuration ' \
                  'Parameters; Reason [%s]' % e
            logger.warning(msg)
            try:
                from be.dparams import DParams
                self._config = DParams
                self._dparams = True
            except Exception, e:
                msg = 'Unable to load Default ' \
                      'Configuration Parameters ' \
                      'for this Project; Reason ' \
                      '[%s]' % e
                logger.error(msg)
                raise
        msg = 'Successfully loaded the configuration; ' \
              'They are as follows: %s' % self._config
        logger.debug(msg)
        return None   
    
    def validConfig(self):
        # NOTE: It is not possible to run 'dev', 'test', 
        #       'release', 'prelease' commands without
        #       running "be configure"
        if (self._target == Tdev       or \
            self._target == Ttest      or \
            self._target == Trelease   or \
            self._target == Tprelease) and \
            self._cparams == False:
            msg = 'Please run \"be configure\" with ' \
                  'sutiable parameters before attempting '\
                  'to %s' % (self._target)
            raise ConfigureParametersNotFound(msg)
        return True

    def getConfig(self):
        return self._config
        
