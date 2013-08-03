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

