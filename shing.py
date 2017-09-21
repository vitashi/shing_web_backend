#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os

from google.appengine.api import memcache
from webapp2 import WSGIApplication, Route
from webapp2_extras.routes import RedirectRoute

from Apis.AccountAPI import account_api
from Apis.UserAPI import user_api
from Apis.PaymentPlanAPI import payment_plan_api
from Apis.PricePlanAPI import price_plan_api

memcache_client = memcache.Client()

# Localhost timezone (datetime.now()) defaults to EAT (Computer Clocks timezone).
# This causes some issues since datastore auto_now is always on UTC
# E.g condition parser tests failing everyday between 0:00 and 3:00 EAT.
# The line below is a quick fix
os.environ['TZ'] = 'UTC'


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'shing-web-backend-key',
}

logging.getLogger().setLevel(logging.DEBUG)

apis = []
apis.extend(user_api)
apis.extend(account_api)
apis.extend(payment_plan_api)
apis.extend(price_plan_api)


app = WSGIApplication(apis, debug=True, config=config)
