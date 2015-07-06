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
        datasetmap = {}
        csvlocation = "data/"
        questionfile = open(os.path.join(csvlocation, 'Questions.csv'), 'rb')
        factfile = open(os.path.join(csvlocation, 'Facts.csv'), 'rb')
        placesfile = open(os.path.join(csvlocation, 'Places.csv'), 'rb')
        questionreader = csv.DictReader(questionfile, delimiter=',')
        factreader = csv.DictReader(factfile, delimiter=',')
        placesreader = csv.DictReader(placesfile, delimiter=',')
        for row in questionreader:
            if row['CategoryDescription'] == category:
                dataset = {"id" : len(datasetmap), "key" : row["FactKey"], "question" : row ['Question'], "answers" : 0}
                if 'Dataset Source' in row:
                    dataset['link'] = row['Dataset Source']
                datasetmap[row["FactKey"]] = dataset
        #currently using name as id :/
        for (i,row) in enumerate(placesreader):
            self.locations[row['Location']] = {"id" : i, "name" : row['Location'], "geometry" : {"type" : "Point", "coordinates" : [row['Lon'], row['Lat']]}, "values" : {} }
        for row in factreader:
            if row['Key'] in datasetmap and row['Location'] in self.locations:
                self.locations[row['Location']]['values'][row['Key']] = row['Value']
                datasetmap[row['Key']]['answers'] = datasetmap[row['Key']]['answers'] + 1
                self.answers = self.answers + 1 
        self.datasets = datasetmap.values()
        self.cleanemptylocations()
        self.cleanemptydatasets()

