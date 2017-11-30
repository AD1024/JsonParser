class Token(object):
    def __init__(self, token_type, value):
        self.tokenType = token_type
        self.value = value

    def get_type(self):
        return self.tokenType

    def get_value(self):
        return self.value

    def set_value(self, v):
        self.value = v

    def __str__(self):
        return 'Type:' + str(self.tokenType) + ' Value: ' + str(self.value)
