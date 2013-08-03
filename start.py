from be.parser import BEParser

p = BEParser()
args = p.parse()
print args

from be.manager import BEConfigManager

cm = BEConfigManager(args)
config = cm.getConfig()
print config

from be.buildengine import BuildEngine

be = BuildEngine(args, config)
be.run()
be.summary()




#        if self._target == Tclean:     self._clean()
#        if self._target == Tcleanall:  self._cleanall()
#        if self._target == Tconfigure: self._configure()
#        if self._target == Tdev:       self._dev()
#        if self._target == Ttest:      self._test()
#        if self._target == Trelease:   self._release()
#        if self._target == Tprelease:  self._prelease()
