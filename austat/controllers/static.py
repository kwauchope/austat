from os import path

from bottle import static_file
import bottle


BASE_DIR = path.dirname(path.realpath(__file__))
STATIC_PATH = path.join(BASE_DIR, '../', 'static')


staticApp = bottle.Bottle()


@staticApp.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=STATIC_PATH)
