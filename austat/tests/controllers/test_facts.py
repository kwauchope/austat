from webtest import TestApp
from austat.controllers import facts


APP = None


def setup_module():
    global APP
    APP = TestApp(facts.factsApp)


def test_fact_without_id_fails():
    res = APP.get('/facts/', expect_errors=True)
    assert res.status_code == 404


def test_fact_with_string_id_fails():
    res = APP.get('/facts/hello', expect_errors=True)
    assert res.status_code == 404


def test_fact_with_invalid_id_reports_bad_input():
    res = APP.get('/facts/-1', expect_errors=True)
    assert res.status_code == 400


def test_fact_with_out_of_range_id_reports_bad_input():
    res = APP.get('/facts/5000', expect_errors=True)
    assert res.status_code == 400


def test_fact_for_dummy_returns_srcs():
    res = APP.get('/facts/0')
    assert res.status_code == 200
    assert len(res.json) > 0
