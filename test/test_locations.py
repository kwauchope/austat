from nose.tools import assert_raises
from austat import locations

def getlocationids(locs):
    ids = []
    for loc in locs:
        ids.append(loc['id'])
    return ids

def test_getlocations():
    lockeys = set(['id', 'name', 'lat', 'lon'])
    locs = locations.getlocations()
    ids = []
    for location in locs:
        assert(lockeys.issubset(set(location.keys())))
        ids.append(location['id'])
    #ensure ids are unique
    assert(len(ids) == len(set(ids)))

def test_getrandomlocations():
    locs = locations.getlocations()
    numlocs = len(locs)
    #test boundaries
    assert(set(getlocationids(locations.getrandomlocations(numlocs))) == set(getlocationids(locs)))
    locations.getrandomlocations(numlocs+1)
    #could take a while, test everything is different
    if numlocs > 1:
        assert(len(set(getlocationids(locations.getrandomlocations(numlocs-1))) == numlocs-1))

