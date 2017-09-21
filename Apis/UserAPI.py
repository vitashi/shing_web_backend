
import utils

from webapp2 import Route

from base import ShingHandler


class User(ShingHandler):
	"""docstring for User"""

	def create(self):
		user_name = self.request.get('user_name')
		account_name = self.request.get('account_name')
		email = self.request.get('email')
		password = self.request.get('password')
		logging.info("Creating account %s" % name)
		if all([name, email, password]):
			name = utils.to_upper(name)
		else:
			print "missing mandatory field"


user_api = [
    Route('/api/user/create', handler=User, handler_method="create", methods=["POST"]),
    ]