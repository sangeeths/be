import json


config = {
    "Directories": [],
    "Email": [],
    "Package": ["tgz", "rpm"],
    "Tag": "",
    "Verbose": False,
    "Virtualenv": ""
}

with open('default.config.be', 'wb') as f:
    json.dump(config, f, indent=4, sort_keys=True)


