#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os

from google.appengine.api import memcache
from webapp2 import WSGIApplication, Route
from webapp2_extras.routes import RedirectRoute

from Apis.AccountAPI import account_api
from Apis.UserAPI import user_api

memcache_client = memcache.Client()

# Localhost timezone (datetime.now()) defaults to EAT (Computer Clocks timezone).
# This causes some issues since datastore auto_now is always on UTC
# E.g condition parser tests failing everyday between 0:00 and 3:00 EAT.
# The line below is a quick fix
os.environ['TZ'] = 'UTC'

logging.getLogger().setLevel(logging.DEBUG)

apis = []
apis.extend(user_api)
apis.extend(account_api)


app = WSGIApplication( apis , debug=True)
