
import logging

import utils

from webapp2 import Route

from base import ShingHandler

from Models.ModelPricePlan import PricePlan


class PricePlanAPI(ShingHandler):
	"""docstring for PricePlanAPI"""

	def create(self):
		name = self.request.get('name')
		amount = self.request.get_range('price')
		level = self.request.get_range('level')
		logging.info("Creating price plan %s" % name)
		if name and (amount is not None) and (level is not None):
			name = utils.to_upper(name)
			PricePlan.create(name=name, amount=amount, level=level)
		else:
			print "missing mandatory field"


price_plan_api = [
    Route('/api/price/create', handler=PricePlanAPI, handler_method="create", methods=["POST"]),
    ]