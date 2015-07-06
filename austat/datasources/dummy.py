from datasource import datasource
import sys
class dummy(datasource):

    def __init__(self):
        datasource.__init__(self, 'Dummy')
        #These will be hardcoded, best tag to use for replace?
        self.datasets = [ {"id" : 0, "key" : "avage", "question" : "Where is the average age {{value}}?", "answers" : 0 },
                          {"id" : 1, "key" : "electorate", "question" : "Where is the electorate {{value}}?", "answers" : 0  },
                          {"id" : 1, "key" : "storyname", "question" : "Where was the ABC story {{value}} located?", "answers" : 0 }
                        ]
        #these can be hardcoded or dynamically populated
        self.locations = { "test" : {"id" : "0", "name" : "test", "geometry" : {"type" : "Point",
                                                                      "coordinates" : [45, 45]
                                                                     },
                                                        "values" : {"avage" : "67",
                                                                    "electorate" : "Melbourne"
                                                                   }
                          }}
        self.cleanemptylocations()
        self.cleanemptydatasets()

