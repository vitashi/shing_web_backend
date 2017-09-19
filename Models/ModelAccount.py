import json

import utils

from google.appengine.api import mail, memcache, search, urlfetch, images
from google.appengine.ext import blobstore, ndb, db

from Models.UserDefinedProps import DecimalProperty, NDBDecimalProperty, SafeReferenceProperty
from Models.ModelPricePlan import PricePlan



class Account(db.Model):
    name = db.StringProperty()
    price_plan = SafeReferenceProperty(PricePlan)
    payment_plan = SafeReferenceProperty(PaymentPlan)
    email = db.StringProperty()
    active = db.BooleanProperty(default=True)
    create_date = db.DateTimeProperty(auto_now_add=True)
    expiry_date = db.DateTimeProperty(auto_now_add=True)
    cutoff_date = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create(name=None, price_plan=None, email=None, payment_plan=None):
    	if all([name, price_plan, email]):
    		name = utils.to_upper(name)
    		expiry_date, cutoff_date = payment_plan.get_expiry_and_cutoff()
    		acc = Account(name=name, price_plan=price_plan, email=email, expiry_date=expiry_date,
    		              cutoff_date=cutoff_date, payment_plan=payment_plan)
    		acc.put()
    		logging.info('Account %s created on plan %s' % (name, price_plan))
    		return True

    @staticmethod
    def fetch(acc_key):
    	if acc_key:
    		return Account.get(acc_key)

    def update(self, name=None, priceplan=None, email=None, active=None, cutoff=None,
               expiry=None, put=True):
    	if name:
    		self.name = utils.to_upper(name)
    	if email:
    		self.email = email
    	if price_plan:
    		self.price_plan = price_plan
    	if active:
    		self.active = active
    	if cutoff:
    		self.cutoff_date = cutoff
    	if expiry:
    		self.expiry_date = expiry
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
        