from webtest import TestApp
from austat.controllers import topics


APP = None


def setup_module():
    global APP
    APP = TestApp(topics.topicsApp)


def test_topics_are_returned():
    res = APP.get('/topics')

    assert res.status_code == 200
    assert len(res.json) > 0
    ids = [x['id'] for x in res.json]

    assert len(ids) == len(set(ids))
