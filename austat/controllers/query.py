import bottle
from bottle import request, response, abort
import json

try:
    from datasources import getsources
except ImportError:
    from austat.datasources import getsources


queryApp = bottle.Bottle()


@queryApp.get('/query/<iden:int>')
def get_qn(iden):
    srcs = getsources()

    if iden < 0 or iden >= len(srcs):
        abort(400, 'Requested source %d but only have %d' % (iden, len(srcs)))

    src = srcs[iden]
    response.content_type = 'application/json'
    #hard coded 'difficulty' for now
    return json.dumps(src.getrandomstat(4))
