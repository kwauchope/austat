try:
    from .csvdatasource import csvdatasource
except ImportError:
    from csvdatasource import csvdatasource


class demographics(csvdatasource):

    def __init__(self):
        csvdatasource.__init__(self, 'Demographics')
        self.loadCSV("Demographics")
