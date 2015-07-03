from datasource import datasource

class dummy(datasource):

    stats = ["test"]

    def getstat(self,stat,n):
        actual = { "locationid" : 0,
                   "name" : stat,
                   "value" : "0"
                 }
        alternatives = []
        for i in range (0,n-1):
            alternatives.append({ "locationid" : i,
                                 "name" : stat,
                                 "value" : i
                               })
        return { "actual" : actual, 
                 "alternatives" : alternatives
               }
