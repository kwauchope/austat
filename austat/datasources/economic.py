from .csvdatasource import csvdatasource


class economic(csvdatasource):

    def __init__(self):
        csvdatasource.__init__(self, 'Economic')
        self.loadCSV("Economic")
