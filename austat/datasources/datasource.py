import random


class datasource(object):

    def __init__(self, name):
        self.datasets = []
        self.locations = []
        if not name:
            raise ValueError('A name is required for a datasource')
        self.name = name


    def getlocations(self):
        return self.locations

    def getdatasets(self):
        return self.datasets

    def getrandomstat(self, n):
        if len(self.datasets) == 0:
            return []
        return self.getstat(random.randint(0, len(self.datasets)-1), n)

    # TODO: could add per stat stdev as an arg to make sure all diff
    def getrandomlocations(self, datasetid, n):
        if n <= 0:
            raise Exception("Need to get at least one location")
        locs = []
        ids = []
        num = min(len(self.locations), n)
        key = self.datasets[datasetid]['key']
        while len(locs) < num:
            index = random.randint(0, len(self.locations)-1)
            if index not in ids:
                ids.append(index)
                loc = self.locations[index]
                if key in loc['values']:
                    locs.append(loc)
            if len(ids) == len(self.locations):
                break
        return locs

    def getstat(self, datasetid, n):
        results = []
        locs = self.getrandomlocations(datasetid, n)
        if len(locs) > 0:
            key = self.datasets[datasetid]['key']
            for loc in locs:
                # don't always have to have an associated value for every
                # location assume most will though if don't this will break
                results.append({"id": loc['id'],
                                "name": loc['name'],
                                "value": loc['values'][key],
                                "geometry": loc['geometry'],
                                })
        return {'question': self.datasets[datasetid]['question'],
                "locations": results}