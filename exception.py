class BEException(Exception):
    def __init__(self, value='Build Engine Exception'):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidDirectory(BEException):
    def __init__(self, value='Invalid Directory'):
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
    

