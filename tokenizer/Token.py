from .TokenEnum import *

class Token(object) :
    def __init__(self, tokenType, value) :
        self.tokenType = tokenType
        self.value = value

    def getType(self) :
        return self.tokenType

    def getValue(self) :
        return self.value

    def setValue(self, value) :
        self.value = v
    
    def __str__(self) :
        return 'Type:' + self.tokenType.name + ' Value: ' + str(self.value)