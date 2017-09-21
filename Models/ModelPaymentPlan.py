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

    def __str__(self):
        return "%s" % (self.name)

    @staticmethod
    def create(name=None, grace_period=None, subscription_period=None):
        payment_plan = PaymentPlan(name=name, grace_period=grace_period,
                                   subscription_period=subscription_period)
        payment_plan.put()

    def update(self, default=None, name=None, grace_period=None, subscription_period=None,
               put=True):
        if name:
            self.name = name
        if grace_period:
            self.grace_period = grace_period
        if subscription_period:
            self.subscription_period = subscription_period
        if default:
            last_default = PaymentPlan.get_default_plan()
            if last_default:
                last_default.deactivate_default()
            self.default = default
        if put:
            self.put

    @staticmethod
    def get_plan(key=None):
        if key:
            return PaymentPlan.get(key)

    @staticmethod
    def get_default_plan():
        plans = PaymentPlan.all().fetch(100)
        plan = filter(lambda x: x.default == True, plans)
        return plan.pop() if plan else None

    def deactivate_default(self):
        self.active = False
        self.put()

    def __get_expiry(self, expiry=None):
        if not expiry:
            expiry = datetime.now()
        expiry = expiry + timedelta(days=self.subscription_period)
        return expiry

    def __get_cutoff(self, expiry=None):
        if expiry:
            cutoff = expiry + timedelta(days=self.grace_period)
            return cutoff

    def get_expiry_and_cutoff(self, expiry=None):
        expiry = self.__get_expiry(expiry)
        cutoff = self.__get_cutoff(expiry)
        return expiry, cutoff
