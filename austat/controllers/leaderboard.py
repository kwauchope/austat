import bottle
from bottle import request, response, abort
from collections import Counter
import json
import itertools
import logging


leaderboardApp = bottle.Bottle()


STATS_CORRECT = Counter()
ATTEMPTS = Counter()


def get_user():
    user = request.headers.get('X-Forwarded-For', request.remote_addr)
    logging.info('USER = %s', user)
    return user

def log_attempt(user, successful):
    if successful:
        STATS_CORRECT[user] += 1
    ATTEMPTS[user] += 1


def get_rank(user):
    if not ATTEMPTS[user]:
        return 0, 0, 0

    ranks = {}
    for u, tot in ATTEMPTS.iteritems():
        correct = STATS_CORRECT.get(u, 0)
        ranks[u] = correct/float(tot), tot

    ranked = sorted(ranks.iteritems(), key=lambda x: x[1], reverse=True)
    user_info = next((x for x in enumerate(ranked, 1) if x[1][0] == user))
    u_rank = user_info[0]
    totals =  len(ATTEMPTS)
    p_correct = user_info[1][1][0]*100
    return u_rank, p_correct, totals


@leaderboardApp.post('/leaderboard')
def update_leaderboard():
    'Adds stats to the leaderboard'
    res = request.query.get('success', '').lower()
    if res != 'true' and res != 'false':
        abort(400, 'success was %r, it should be true or false' %
              request.query.get('success', ''))
    log_attempt(get_user(), res == 'true')


@leaderboardApp.get('/leaderboard')
def get_rankings():
    'Gets the sorted rankings from the leaderboard'
    response.content_type = 'application/json'
    rank, p_correct, total = get_rank(get_user())
    resp = {
        'rank': rank,
        'percent_correct': p_correct,
        'total': total
    }
    return json.dumps(resp)
