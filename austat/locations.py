import random

#hard coded locations of interest
locations= [{"id" : 0, "name" : "test", "lat" : 45, "lon" : 45}]

def getlocations():
    return locations

def getrandomlocations(n):
    if n <= 0:
        raise Exception("Need to get at least one location")
    if n == len(locations):
        return locations
    locs = []
    ids = []
    num = min(len(locations), n)
    while len(locs) < num:
        index = random.randint(0, len(locations)-1)
        if index not in ids:
            ids.append(index)
            locs.append(locations[index])
