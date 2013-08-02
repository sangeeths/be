import json


config = {
    "BECompileDirectories" : [],
    "BEPackage" : ["tgz", "rpm"],
    "BEEmail" : [],
    "BETag" : "",
    "BEVerbose": False,
    "BERequirements" : "REQUIREMENTS"
}

with open('default.config.be', 'wb') as f:
    json.dump(config, f)


