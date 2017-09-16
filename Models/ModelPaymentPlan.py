import json

import utils

from datetime import datetime, timedelta
from google.appengine.api import mail, memcache, search, urlfetch, images
from google.appengine.ext import blobstore, ndb, db

from Models.UserDefinedProps import DecimalProperty, NDBDecimalProperty, SafeReferenceProperty


class PaymentPlan(db.Model):
    name = db.StringProperty()
    grace_period = db.IntegerProperty()
    subscription_period = db.IntegerProperty(default=1)

    def __str__(self)
        return "%s" % (self.name)

    @staticmethod
    def create(name=None, grace_period=None, subscription_period=None):
        payment_plan = PaymentPlan(name=name, grace_period=grace_period,
                                   subscription_period=subscription_period)
        payment_plan.put()

    def update(self, name=name, grace_period=None, subscription_period=None, put=True):
        if name:
            self.name = name
        if grace_period:
            self.grace_period = grace_period
        if subscription_period:
            self.subscription_period = subscription_period
        if put:
            self.put

    @staticmethod
    def get_plan(key=None):
        if key:
            return PaymentPlan.get(key)

    def __get_expiry(self, initial=None):
        expiry = datetime.now()
        if not initial:
            expiry = expiry + timedelta(days=self.subscription_period)
        return expiry

    def __get_cutoff(self, expiry=None):
        if not expiry:
            expiry = datetime.now()
        cutoff = expiry + timedelta(days=self.grace_period)

    def get_expiry_and_cutoff(self, initial=None):
        expiry = self.__get_expiry(initial)
        cutoff = self.__get_cutoff(expiry)
        return expiry, cutoff
