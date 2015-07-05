from datasource import datasource
import csv
import os

import sys
import json

class csvdatasource(datasource):

    #csvlocation = None

    def __init__(self, name):
        datasource.__init__(self, name)
    #    csvlocation = "../../data/"

    def loadCSV(self, category):
        csvlocation = "data/"
        questionfile = open(os.path.join(csvlocation, 'Questions.csv'), 'rb')
        factfile = open(os.path.join(csvlocation, 'Facts.csv'), 'rb')
        placesfile = open(os.path.join(csvlocation, 'Places.csv'), 'rb')
        questionreader = csv.DictReader(questionfile, delimiter=',')
        factreader = csv.DictReader(factfile, delimiter=',')
        placesreader = csv.DictReader(placesfile, delimiter=',')
        keys = []
        for row in questionreader:
            if row['CategoryDescription'] == category:
                dataset = {"key" : row['FactKey'], "question" : row ['Question']}
                if 'Dataset Source' in row:
                    dataset['link'] = row['Dataset Source']
                self.datasets.append(dataset)
                keys.append(row['FactKey'])
        #currently using name as id :/
        for (i,row) in enumerate(placesreader):
            self.locations[row['Location']] = {"id" : i, "name" : row['Location'], "geometry" : {"type" : "Point", "coordinates" : [row['Lon'], row['Lat']]}, "values" : {} }
        for row in factreader:
            if row['Key'] in keys and row['Location'] in self.locations:
                self.locations[row['Location']]['values'][row['Key']] = row['Value']
        self.cleanemptylocations()
        self.cleanemptydatasets()
        #sys.stderr.write(json.dumps(self.locations))
        #sys.stderr.write(json.dumps(self.datasets))

