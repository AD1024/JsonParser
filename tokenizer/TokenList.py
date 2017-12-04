class TokenList(object):
    def __init__(self):
        self.tokenList = list()
        self.cursor = 0

    def get_cursor_position(self):
        return self.cursor

    def append(self, token):
        self.tokenList.append(token)

    def next(self):
        ret = self.tokenList[self.cursor]
        self.cursor += 1
        return ret

    def has_next(self):
        return self.cursor < len(self.tokenList)

    def current_token(self):
        if self.has_next():
            return self.tokenList[self.cursor]
        else:
            return None

    def prev_token(self, gen):
        if self.cursor == 0:
            return None
        return self.tokenList[self.cursor - gen]
