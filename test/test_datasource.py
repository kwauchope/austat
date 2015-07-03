from austat import datasources
from austat import locations

def test_getsources():
    datasources.__all__

def test_getrandomstat():
    statkeys = set(['locationid', 'name', 'value'])
    for datasource in datasources.__all__:
        module = __import__("austat.datasources."+datasource, fromlist=[datasource])
        ds = getattr(module, datasource)()
        #select number of locations based on length of whats available
        numlocations = len(locations.getlocations())
        #numalternates = locations.getlocations
        res = ds.getrandomstat(numlocations)
        assert(res['actual'] is not None)
        assert(res['alternatives'] is not None)
        assert(len(res['alternatives']) == numlocations - 1)
        assert(statkeys.issubset(set(res['actual'].keys())))
        for alternate in res['alternatives']:
            assert(statkeys.issubset(set(alternate.keys())))

