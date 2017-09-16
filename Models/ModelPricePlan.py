import json

import utils

from google.appengine.api import mail, memcache, search, urlfetch, images
from google.appengine.ext import blobstore, ndb, db

from Models.UserDefinedProps import DecimalProperty, NDBDecimalProperty, SafeReferenceProperty
from Models.config import DEFAULT_PRICE_PLANS


class PricePlan(db.Model):
    name = db.StringProperty()
    amount = db.IntegerProperty()
    level = db.IntegerProperty()
    create_date = db.DateTimeProperty(auto_now_add=True)
    active = db.BooleanProperty(default=True, indexed=True)

    @staticmethod
    def auto_create():
    	"""
    	Creates Price plans
    	"""
    	logging.info("Initializing Price plans")
    	pplans = []
    	for level, values in DEFAULT_PRICE_PLANS.iteritems():
    		plan = PricePlan(name=utils.to_upper(values.get('name')),
    		                 amount=values.get('price'),
    		                 level=level)
    		pplans.append(plan)
    	db.put(pplans)

    @staticmethod
    def fetch(key=None, name=None):
    	if key:
    		return PricePlan.get(key)
    	elif name:
    		return PricePlan.all().filter('name =', utils.to_upper(name)
    		                              ).get()

    def update(self, name=None, active=None, amount=None):
    	if name:
    		self.name = utils.to_upper(name)
    	if active:
    		self.active = active
    	if amount:
    		self.amount = amount

    @staticmethod
    def get_all_active():
    	return PricePlan.all().filter('active = ', True).fetch(50)  # may never grow to even 10

    def get_all_inactive():
    	return PricePlan.all().filter('active =', False).fetch(50)  # may never grow to even 10

    def can_be_archived():
    	all_active = PricePlan.get_all_active()
    	return all_active > 0

    def __str__(self):
        return "%s" % (self.name)