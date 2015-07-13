try:
    from .csvdatasource import csvdatasource
except ImportError:
    from csvdatasource import csvdatasource

class economic(csvdatasource):

    def __init__(self):
        csvdatasource.__init__(self, 'Economics')
        self.loadCSV("Economics")
