#!/usr/bin/python

import webbrowser
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import facebook

from db_module import add_new_user

PORT_NUMBER = 8000
APP_ID = 222805424880776
APP_SECRET = '36f97d6ee25af24899a40b3124b5ff9f'
REDIRECT_URL = 'http://localhost:8000/'

# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        if '?code' in self.path:
            graph = facebook
            z = graph.GraphAPI(version='2.3')
            code = self.path.split('=')[1]
            r = z.get_access_token_from_code(code=code, app_id=APP_ID, redirect_uri=REDIRECT_URL, app_secret=APP_SECRET)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Send the html message
            graph = facebook.GraphAPI(r['access_token'])
            w = graph.get_object('me')
            add_new_user(r['access_token'], w)
            self.wfile.write("New User %s Added. You can close this tab" % w['name'])
            # graph = facebook.GraphAPI(r['access_token'])
            # extended_token = graph.extend_access_token(APP_ID, APP_SECRET)
            # print extended_token
            return


class Server:
    def __init__(self):
        try:
            # Create a web server and define the handler to manage the
            # incoming request
            server = HTTPServer(('', PORT_NUMBER), myHandler)
            print 'Started httpserver on port ', PORT_NUMBER

            # Wait forever for incoming htto requests
            server.serve_forever()

        except KeyboardInterrupt:
            print '^C received, shutting down the web server'
            server.socket.close()
