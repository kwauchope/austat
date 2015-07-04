import bottle
from bottle import request, response, abort
import json

try:
    from datasources import available_sources
except ImportError:
    from austat.datasources import available_sources

topicsApp = bottle.Bottle()


TOPICS = available_sources()


@topicsApp.get('/topics')
def get_topics():
    response.content_type = 'application/json'
    return json.dumps(TOPICS)
