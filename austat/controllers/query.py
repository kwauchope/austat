import bottle
from bottle import request, response, abort
import json

from datasources import getsources


queryApp = bottle.Bottle()


@queryApp.get('/query/<iden:int>')
def get_qn(iden):
    srcs = getsources()

    try:
        src = srcs[iden]
    except IndexError:
        abort(400, 'Requested source %d but only have %d' % (iden, len(srcs)))
    else:
        response.content_type = 'application/json'
        return json.dumps(src.getrandomstat(6))
