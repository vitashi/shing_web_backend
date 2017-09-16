#!/usr/bin/python
# -*- coding: utf-8 -*-
import decimal
import logging
from google.appengine.ext import db, ndb

precision = decimal.Decimal(10) ** -5  # Precision for db is 5 decimal places


class SafeReferenceProperty(db.ReferenceProperty):

    def __get__(self, model_instance, model_class):
        try:
            return super(SafeReferenceProperty, self).__get__(
                model_instance, model_class)
        except Exception, ex:
            logging.warning([ex, model_instance.key()])
        return None


class DecimalProperty(db.TextProperty):
    data_type = decimal.Decimal

    def validate(self, value):
        value = super(DecimalProperty, self).validate(value)
        if value is None or isinstance(value, decimal.Decimal):
            return value
        elif isinstance(value, basestring):
            return decimal.Decimal(value)
        raise db.BadValueError(
            "Property %s must be a Decimal or string." % self.name)

    def get_value_for_datastore(self, model_instance):
        vfd = super(DecimalProperty, self).get_value_for_datastore(
            model_instance)
        decimal.getcontext().prec = 28
        return str(vfd.quantize(precision)) if vfd is not None else None

    def make_value_from_datastore(self, value):
        if value is not None and value != 'None':
            return decimal.Decimal(value)


class NDBDecimalProperty(ndb.TextProperty):

    def _validate(self, value):
        if not isinstance(value, (decimal.Decimal, str)):
            raise db.BadValueError(
                'Expected decimal or string, got %r' % (value,))

        return decimal.Decimal(value)

    def _to_base_type(self, v):
        return str(v)

    def _from_base_type(self, v):
        return decimal.Decimal(v)