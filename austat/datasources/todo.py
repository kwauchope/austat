from csvdatasource import csvdatasource


class todo(csvdatasource):

    def __init__(self):
        csvdatasource.__init__(self, 'ToDo')
        self.loadCSV("TODO")
