import random


class datasource(object):

    def __init__(self, name):
        self.datasets = []
        self.locations = {}
        self.answers = 0
        if not name:
            raise ValueError('A name is required for a datasource')
        self.name = name

    #clean datasets so don't get crap stuff
    def cleanemptydatasets(self):
        self.datasets = [x for x in self.datasets if x['answers'] > 0]

    #clean empty locations to save mem
    def cleanemptylocations(self):
        todel = []
        for name, location in self.locations.iteritems():
            if len(location['values']) == 0:
                todel.append(name)
        for name in todel:
            del self.locations[name]

    def getlocations(self):
        return self.locations.values()

    def getdatasets(self):
        return self.datasets

    def getrandomstat(self, n):
        if len(self.datasets) == 0:
            return []
        return self.getstat(random.randint(0,len(self.datasets) -1), n)

    # TODO: could add per stat stdev as an arg to make sure all diff
    def getrandomlocations(self, datasetkey, n):
        if n <= 0:
            raise Exception("Need to get at least one location")
        locs = []
        ids = {}
        lockeys = self.locations.keys()
        num = min(len(lockeys), n)
        while len(locs) < num:
            possible = random.choice(lockeys)
            if possible not in ids:
                ids[possible] = 1
                loc = self.locations[possible]
                if datasetkey in loc['values']:
                    locs.append(loc)
            if len(ids) == len(lockeys):
                break
        return locs

    def getmatchinglocations(self, datasetkey, n):
        if n <= 0:
            raise Exception("Need to get at least one location")
        locs = []
        num = min(len(self.locations), n)
        for loc in self.locations.values():
            if datasetkey in loc['values']:
                locs.append(loc)
            if len(locs) == num:
                break
        return locs

    def getstat(self, datasetid, n):
        dataset = self.datasets[datasetid]
        results = []
        datasetkey = dataset['key']
        locs = self.getrandomlocations(datasetkey, n)
        if len(locs) > 0:
            for loc in locs:
                results.append({"id": loc['id'],
                                "name": loc['name'],
                                "value": loc['values'][datasetkey],
                                "geometry": loc['geometry'],
                               })
        response = {'question': dataset['question'],
                "locations": results}
        if 'link' in dataset:
            response['link'] = dataset['link']
        return response
