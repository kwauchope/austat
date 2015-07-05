from .csvdatasource import csvdatasource


class social(csvdatasource):

    def __init__(self):
        csvdatasource.__init__(self, 'Social')
        self.loadCSV("Social")
