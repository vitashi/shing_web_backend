import json

import utils

from google.appengine.api import mail, memcache, search, urlfetch, images
from google.appengine.ext import blobstore, ndb, db

from Models.UserDefinedProps import DecimalProperty, NDBDecimalProperty, SafeReferenceProperty
from Models.ModelPricePlan import PricePlan
from Models.ModelAccount import Account
from Models.ModelPaymentPlan import PaymentPlan


class Subscription(db.Model):
    name = db.StringProperty()
    price_plan = SafeReferenceProperty(PricePlan)
    account = SafeReferenceProperty(Account)
    payment_plan = SafeReferenceProperty(PaymentPlan)
    create_date = db.DateTimeProperty(auto_now_add=True)
    expiry_date = db.DateTimeProperty(auto_now_add=True)
    cutoff_date = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create(price_plan=None, payment_plan=None, account=None):
    	expiry = None

    	if not payment_plan:
    		payment_plan = PaymentPlan.get_default_plan()
    	if not payment_plan:
    		logging.warning('Could not create Subscription because we do not have a default plan')
    		return

    	last_sub = Subscription.get_last_subscription(account)
    	if last_sub:
    		expiry = last_sub.expiry_date
    	expiry_date, cutoff_date = payment_plan.get_expiry_and_cutoff(expiry)

    	name = '%s from %s to %s' % (price_plan, expiry_date, cutoff_date)
    	sub = Subscription(name=name, price_plan=price_plan, payment_plan=payment_plan,
    	                   expiry_date=expiry_date, cutoff_date=cutoff_date)
    	logging.info("New subscription for %s %s" % (account, name))
    	sub.put()

    @staticmethod
    def get_last_subscription(account):
    	sub = None
    	if account:
    		sub = Subscription.all().filter("account =", account).order('-create_date').get()
    	return sub

    @staticmethod
    def fetch(sub_key):
    	if sub_key:
    		return Subscription.get(sub_key)

    @staticmethod
    def get_all_subscriptions():
    	subs = Subscription.all().fetch(300)
    	return subs

    @staticmethod
    def get_all_subscriptions_by_account(account):
    	subs = Subscription.all().filter('account =', account).fetch(300)
    	return subs

    def __str__(self):
        return "%s" % (self.name)
        