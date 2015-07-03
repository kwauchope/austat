#!/usr/bin/env python


import logging

import begin
from bottle import route, run

@route('/hello')
def hello():
    return "Hello World!"


@begin.start
@begin.logging
@begin.convert(port=int, debug=bool)
def main(hostname='0.0.0.0', port=8080, debug=True):
        run(host=hostname, port=port, debug=debug)
