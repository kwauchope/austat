from webtest import TestApp

import austat

APP = None

def setup_module(module):
    global APP
    APP = TestApp(austat.app)


def test_hi():
    assert APP.get('/hello').status == '200 OK'
