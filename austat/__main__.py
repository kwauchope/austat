#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()


import begin
import bottle

from controllers.leaderboard import leaderboardApp
from controllers.topics import topicsApp
from controllers.query import queryApp
from controllers.static import staticApp


def create_app():
    app = bottle.app()
    app.merge(leaderboardApp)
    app.merge(topicsApp)
    app.merge(queryApp)
    app.merge(staticApp)

    return app


@begin.start
@begin.logging
@begin.convert(port=int, debug=bool, dev=bool)
def main(hostname='0.0.0.0', port=8080, dev=True, debug=True):
    """
    Start up the service

    hostname: Defines what ip and consequently which interface to bind to.

    port: The service port

    dev: Runs bottle with auto reloading enabled

    debug: Log requests
    """
    app = create_app()
    app.run(host=hostname, port=port, debug=debug, reloader=dev, server="gevent")
