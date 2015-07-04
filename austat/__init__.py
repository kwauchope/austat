#!/usr/bin/env python


from os import path

import begin
from bottle import run, static_file
import bottle


BASE_DIR = path.dirname(path.realpath(__file__))
STATIC_PATH = path.join(BASE_DIR, 'static')


app = bottle.app()


@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=STATIC_PATH)


@app.route('/hello')
def hello():
    return "Hello World!"


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
    run(host=hostname, port=port, debug=debug, reloader=dev, app=app)
