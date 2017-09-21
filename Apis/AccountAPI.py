
from webapp2 import Route

from base import ShingHandler


class Account(ShingHandler):
	"""docstring for Account"""

	def create(self):
		print "Hello Shing"
		self.response.write("Hello Shing")


account_api = [
    Route('/api/account/create', handler=Account, handler_method="create", methods=["POST"]),
    Route('/', handler=Account, handler_method="create", methods=["GET"]),
    ]
