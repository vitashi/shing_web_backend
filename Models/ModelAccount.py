import json

import utils

from google.appengine.api import mail, memcache, search, urlfetch, images
from google.appengine.ext import blobstore, ndb, db

from Models.UserDefinedProps import DecimalProperty, NDBDecimalProperty, SafeReferenceProperty
from Models.ModelPricePlan import PricePlan


class Account(db.Model):
    name = db.StringProperty()
    email = db.StringProperty()
    active = db.BooleanProperty(default=True)
    create_date = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create(name=None, email=None):
    	if all([name, email]):
    		name = utils.to_upper(name)
    		acc = Account(name=name, email=email)
    		acc.put()
    		logging.info('Account %s created on plan %s' % (name, email))
    		return True

    @staticmethod
    def fetch(acc_key):
    	if acc_key:
    		return Account.get(acc_key)

    def update(self, name=None, email=None):
    	if name:
    		self.name = utils.to_upper(name)
    	if email:
    		self.email = email
    	if put:
    		self.put()
    		logging.info('Account %s updated' % self)

    @staticmethod
    def get_all_active():
    	return Account.all().filter('active =', True).fetch(300)

    @staticmethod
    def get_all_inactive():
    	return Account.all().filter('active =', False).fetch(300)

    def __str__(self):
        return "%s" % (self.name)
        