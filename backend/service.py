#!/usr/bin/env python


import logging

import begin
from bottle import route, run

@route('/hello')
def hello():
    return "Hello World!"


@begin.start
@begin.logging
@begin.convert(port=int)
def main(hostname='0.0.0.0', port=8080):


        run(host='localhost', port=8080, debug=True)
