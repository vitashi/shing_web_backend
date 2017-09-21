import json

import utils

from google.appengine.api import mail, memcache, search, urlfetch, images
from google.appengine.ext import blobstore, ndb, db

from Models.UserDefinedProps import DecimalProperty, NDBDecimalProperty, SafeReferenceProperty
from Models.ModelAccount import Account


class User(db.Model):
    name = db.StringProperty()
    email = db.StringProperty()
    salt = db.StringProperty(indexed=False)
    sha = db.StringProperty(indexed=False)
    account = SafeReferenceProperty(Account)
    active = db.BooleanProperty(default=True)
    create_date = db.DateTimeProperty(auto_now_add=True)
    update_date = db.DateTimeProperty(auto_now_add=True)
    last_login = db.DateTimeProperty(auto_now_add=True)
    pw_update_date = db.DateTimeProperty(auto_now_add=True)

    def __str__(self):
    	return "%s" % self.name

    def setPassword(self, user_password=None):
        if user_password:
            user_password = user_password.strip()
            self.salt, self.sha = utils.getSHA(user_password, self.salt)
            self.pw_update_date = datetime.now()

    def validate(self, password):
    	password = password.strip()
	    salt, sha = utils.getSHA(password, self.salt)
	    if self.salt == salt:
	    	return True

    @staticmethod
    def create(name=None, email=None, account=None, password=None):
    	if all([name, account, password, email]):
    		name = utils.to_upper(name)
    		user = User(name=name, email=email, account=account, salt=salt, sha=sha, active=active)
    		user.put()
    		logging.info('User %s on %s created' % (name, account))
    		return True

    @staticmethod
    def fetch_account_users(account=None):
    	users = None
    	if account:
    		users = User.all().filter('account =', account).fetch(500)
    	return users

    def update(self, name=None, email=None, active=None, password=None, new_password=None, put=True):
    	if any([name, email, active, password]):
	    	if name:
	    		self.name = utils.to_upper(name)
	    	if email:
	    		self.email = email
	    	if active:
	    		self.active = active
	    	if password and self.validate(password):
	    		self.setPassword(password)
	    	self.update_date = datetime.now()
    	if put:
    		self.put()
    		logging.info('User %s updated' % self)

    @staticmethod
    def get_all_active():
    	return User.all().filter('active =', True).fetch(300)

    @staticmethod
    def get_all_inactive():
    	return User.all().filter('active =', False).fetch(300)
        