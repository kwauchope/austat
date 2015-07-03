import random

#hard coded locations of interest
locations= [{"id" : 0 , "name" : "test",  "lat" : 45, "lon" : 45}]

def getlocations():
    return locations

def getrandomlocations(n):
    if n <= 0:
        raise Exception("Need to get at least one location")
    if n > len(locations):
        raise Exception("Asking for more locations than is available")
    if n == len(locations):
        return locations
    locs = []
    ids = []
    while len(locs) < n:
        index = random.randint(0,len(locations)-1)
        if index not in ids:
            ids.append(index) 
            locs.append(locations[index])
