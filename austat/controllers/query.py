import bottle
from bottle import request, response, abort
import json

try:
    from datasources import getsources
except ImportError:
    from austat.datasources import getsources


queryApp = bottle.Bottle()


@queryApp.get('/query/<iden:int>')
@queryApp.get('/query/<iden:int>/<fact:int>')
def get_qn(iden, fact=None):
    srcs = getsources()

    if iden < 0 or iden >= len(srcs):
        abort(400, 'Requested source %d but only have %d' % (iden, len(srcs)))
    src = srcs[iden]

    if fact and (fact < 0 or fact >= len(src.getdatasets())):
        abort(400, 'Requested facts %d but only have %d' % (iden, len(src.getdatasets())))
    
    response.content_type = 'application/json'
    #hard coded 'difficulty' for now
    if fact is not None:
        return json.dumps(src.getstat(fact,4))
    else:
        return json.dumps(src.getrandomstat(4))
