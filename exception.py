class BEException(Exception):
    def __init__(self, value='Build Engine Exception'):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidRootDirectory(BEException):
    def __init__(self, value='Invalid Root Directory'):
        self.value = value
    
class InvalidCompileDirectory(BEException):
    def __init__(self, value='Invalid Compile Directory'):
        self.value = value
    
class InvalidEmailID(BEException):
    def __init__(self, value='Invalid Email Address'):
        self.value = value
    
class InvalidPackage(BEException):
    def __init__(self, value='Invalid Package'):
        self.value = value
    
class InvalidTag(BEException):
    def __init__(self, value='Invalid Tag'):
        self.value = value
    
class GetProjectDefaultConfigFailed(BEException):
    def __init__(self, value='Unable to get the project default configurations'):
        self.value = value
    
class GetProjectConfigureParametersFailed(BEException):
    def __init__(self, value='Unable to get the project configuration parameters'):
        self.value = value

class ValueNotFound(BEException):
    def __init__(self, value='Value Not Found'):
        self.value = value





# -----------------------------------------------

class ConfigureParametersNotFound(BEException):
    def __init__(self, value='Configure Parameters Not Found'):
        self.value = value

class InvalidConfiguration(BEException):
    def __init__(self, value='Invalid Configuration'):
        self.value = value

class TargetCleanFailed(BEException):
    def __init__(self, value='Clean Failed'):
        self.value = value

class TargetConfigureFailed(BEException):
    def __init__(self, value='Configuration Failed'):
        self.value = value

class GenerateTgzFailed(BEException):
    def __init__(self, value='Generating Tzg Failed'):
        self.value = value

class GenerateMD5SumFailed(BEException):
    def __init__(self, value='Generating md5sum Failed'):
        self.value = value

class UnableToIgnoreItem(BEException):
    def __init__(self, value='Unable to Ignore'):
        self.value = value

class UnableToAddPackageFiles(BEException):
    def __init__(self, value='Unable to Add Files to Package'):
        self.value = value

