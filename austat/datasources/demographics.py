from csvdatasource import csvdatasource

class demographics(csvdatasource):

    def __init__(self):
        csvdatasource.__init__(self)
        self.loadCSV("Demographics")
