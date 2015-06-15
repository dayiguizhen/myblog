#! /use/bin/python

from flup.server.fcgi import WSGIServer
from manage import app

if __name__ == '__main__':
    WSGIServer(app,bindAddress = ('127.0.0.1',5000)).run()
