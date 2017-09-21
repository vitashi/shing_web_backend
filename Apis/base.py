import logging
import webapp2

logging.getLogger().setLevel(logging.DEBUG)

class ShingHandler(webapp2.RequestHandler):
	def __init__(self, request, response):
		self.initialize(request, response)


class ApiChecker():
	pass


def request_logger():
	pass