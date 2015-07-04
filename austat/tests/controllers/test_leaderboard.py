from webtest import TestApp
from austat.controllers import leaderboard


APP = None


def assert_data(data, rank, percent, total_users):
    assert data == {
        'rank': rank,
        'percent_correct': float(percent),
        'total': total_users
    }


def setup_module():
    global APP
    APP = TestApp(leaderboard.leaderboardApp)


def test_initial_ranks_make_sense():
    res = APP.get('/leaderboard')
    assert res.status == '200 OK'
    assert_data(res.json, 0, 0, 0)


def test_non_bool_success_raises_bad_request():
    res = APP.post('/leaderboard?success=Foo', expect_errors=True)
    assert res.status_code == 400


def test_no_success_raises_bad_request():
    res = APP.post('/leaderboard', expect_errors=True)
    assert res.status_code == 400


def test_post_updates_totals():
    res = APP.post('/leaderboard?success=True')

    assert res.status == '200 OK'

    res = APP.get('/leaderboard')
    assert_data(res.json, 1, 100, 1)


def test_post_failure_updates_totals():
    res = APP.post('/leaderboard?success=false')

    assert res.status == '200 OK'

    res = APP.get('/leaderboard')
    assert_data(res.json, 1, 50, 1)


def test_post_failure_updates_totals_with_new_user():
    user = {'X-Forwarded-For':'200.12.32.1'}
    res = APP.post('/leaderboard?success=false', headers=user)

    assert res.status == '200 OK'

    res = APP.get('/leaderboard', headers=user)
    assert_data(res.json, 2, 0, 2)
