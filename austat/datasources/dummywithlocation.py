from datasource import datasource
from .. import locations

class dummywithlocation(datasource):

    stats = ["s1"]

    def getstat(self,stat,n):
        randloc = locations.getrandomlocations(n)
        actual = { "locationid" : randloc[0]['id'],
                   "name" : stat,
                   "value" : "0"
                 }
        alternatives = []
        for loc in randloc[1:]:
            alternatives.append({ "locationid" : loc['id'],
                                 "name" : stat,
                                 "value" : i
                                })
        return { "actual" : actual,
                 "alternatives" : alternatives
               }

