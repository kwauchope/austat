#generic datasource test

from austat import datasources
from nose.tools import assert_raises

#Only initialise each list once as can be dynamic with URL calls etc
_globals = {'dslist' : None}

def getsources():
    if _globals['dslist'] is None:
        dslist = datasources.getsources()
    return dslist

def test_available_sources():
    srckeys = set(['id', 'name'])
    ids = []
    for src in datasources.available_sources():
        assert(srckeys.issubset(set(src.keys())))
        ids.append(src['id'])
    #ensure ids are unique
    assert(len(ids) == len(set(ids)))

def test_locations():
    lockeys = set(['id', 'name', 'geometry', 'values'])
    for source in getsources():
        locs = source.getlocations()
        assert(len(locs) > 0)
        ids = []
        for location in locs:
            assert(lockeys.issubset(set(location.keys())))
            assert(len(location['values'].keys()) > 0)
            ids.append(location['id'])
        #ensure ids are unique
        assert(len(ids) == len(set(ids)))

def test_datasets():
    datakeys = set(['id', 'key', 'question', 'answers'])
    for source in getsources():
        ids = []
        datasets = source.getdatasets()
        assert(len(datasets) > 0)
        for dataset in datasets:
            assert(datakeys.issubset(set(dataset.keys())))
            ids.append(dataset['id'])
        #ensure ids are unique
        assert(len(ids) == len(set(ids)))

def getlocationids(locs):
    ids = []
    for loc in locs:
        ids.append(loc['id'])
    return ids

def test_getrandomlocations():
    for source in getsources():
        locs = source.getlocations()
        numlocs = len(locs)
        if numlocs > 1:
            datasets = source.getdatasets()
            for i in range(0, len(datasets)):
                #can't see method - due to dynamic loading?
                #assert_raises(Exception, source, getrandomlocations, i, 0)
                #assert_raises(Exception, source, getrandomlocations, i, -1)
                randomlocs = getlocationids(source.getrandomlocations(i, numlocs))
                #ensure get unique locations
                assert(len(set(randomlocs)) == len(randomlocs))
                #can't return more than have
                assert(len(randomlocs) <= numlocs)

def test_getstat():
    for source in getsources():
        numlocs = len(source.getlocations())
        datasets = source.getdatasets()
        if numlocs > 1:
            for i in range(0, len(datasets)):
                res = source.getstat(i, numlocs)
                assert(res['question'] is not None)
                assert(res['locations'] is not None)

def test_getrandomstat():
    for datasource in getsources():
        numlocs = len(datasource.getlocations())
        if numlocs > 1:
            assert(len(datasource.getrandomstat(numlocs-1)) <= numlocs -1)
