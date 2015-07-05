from datasource import datasource

class dummy(datasource):

    def __init__(self):
        datasource.__init__(self, 'Dummy')
        #These will be hardcoded, best tag to use for replace?
        self.datasets = [{"key" : "avage", "question" : "Where is the average age {{value}}?" },
                         {"key" : "electorate", "question" : "Where is the electorate {{value}}?" },
                         {"key" : "storyname", "question" : "Where was the ABC story {{value}} located?" }
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

