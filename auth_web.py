#! /usr/bin/env python
from alexa_client.settings import PRODUCT_ID, CLIENT_ID, CLIENT_SECRET, WEB_PORT
import cherrypy
import json
import os
import requests
import urllib
import uuid


class Start(object):
    def index(self):
        sd = json.dumps({
            "alexa:all": {
                "productID": PRODUCT_ID,
                "productInstanceAttributes": {
                    "deviceSerialNumber": uuid.getnode()
                }
            }
        })
        url = "https://www.amazon.com/ap/oa"
        callback = cherrypy.url() + "authresponse"
        payload = {
            "client_id": CLIENT_ID,
            "scope": "alexa:all",
            "scope_data": sd,
            "response_type": "code",
            "redirect_uri": callback
        }
        req = requests.Request('GET', url, params=payload)
        p = req.prepare()
        raise cherrypy.HTTPRedirect(p.url)

    def authresponse(self, var=None, **params):
        code = urllib.quote(cherrypy.request.params['code'])
        callback = cherrypy.url()
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": callback
        }
        url = "https://api.amazon.com/auth/o2/token"
        r = requests.post(url, data=payload)
        resp = r.json()
        return "Success! Here is your refresh token:<br>{}".format(
            resp['refresh_token'])

    index.exposed = True
    authresponse.exposed = True


cherrypy.config.update({'server.socket_host': 'localhost'})
cherrypy.config.update({'server.socket_port': WEB_PORT})
print('Open http://localhost:3000 to login in amazon alexa service')
cherrypy.quickstart(Start())
