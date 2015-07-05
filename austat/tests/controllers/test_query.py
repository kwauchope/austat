from webtest import TestApp
from austat.controllers import query


APP = None


def setup_module():
    global APP
    APP = TestApp(query.queryApp)


def test_query_without_id_fails():
    res = APP.get('/query/', expect_errors=True)
    assert res.status_code == 404


def test_query_with_string_id_fails():
    res = APP.get('/query/', expect_errors=True)
    assert res.status_code == 404


def test_query_with_invalid_id_reports_bad_input():
    res = APP.get('/query/-1', expect_errors=True)
    assert res.status_code == 400


def test_query_with_out_of_range_id_reports_bad_input():
    res = APP.get('/query/5000', expect_errors=True)
    assert res.status_code == 400


def test_query_for_dummy_returns_srcs():
    res = APP.get('/query/0')
    assert res.status_code == 200
    assert len(res.json['locations']) > 0
    assert len(res.json['question']) > 0
