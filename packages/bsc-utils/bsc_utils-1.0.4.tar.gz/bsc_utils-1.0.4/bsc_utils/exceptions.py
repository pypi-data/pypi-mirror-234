class NotDatabaseError(Exception):
    pass


class SymbolNotFoundError(Exception):

    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return f'{self.symbol} not exists.'