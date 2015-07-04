from datasource import datasource
import csv
import os

class csvdatasource(datasource):

    #csvlocation = None

    def __init__(self, name):
        datasource.__init__(self, name)
    #    csvlocation = "../../data/"

    def loadCSV(self, category):
        csvlocation = "data/"
        questionfile = open(os.path.join(csvlocation, 'Questions.csv'), 'rb')
        factfile = open(os.path.join(csvlocation, 'Facts.csv'), 'rb')
        placesfile = open(os.path.join(csvlocation,'Places.csv'), 'rb')
        questionreader = csv.DictReader(questionfile, delimiter=',')
        factreader = csv.DictReader(factfile, delimiter=',')
        placesreader = csv.DictReader(placesfile, delimiter=',')
        keys = []
        for row in questionreader:
            if row['CategoryDescription'] == category:
                self.datasets.append({"key" : row['FactKey'], "question" : row ['Question']})
                keys.append(row['FactKey'])
        i = 0
        #currently useing name as id :/
        locs = []
        for row in placesreader:
            self.locations.append({"id" : i, "name" : row['Location'], "geometry" : { "type" : "Point", "coordinates" : [row['Lon'], row['Lat']]}, "values" : {} })
            locs.append(row['Location'])
            i = i+1
        for row in factreader:
            if row['Key'] in keys and row['Location'] in locs:
                #have to loop due to data layout
                for loc in self.locations:
                    if loc['name'] == row['Location']:
                        loc['values'][row['Key']] = row['Value']
                        break

