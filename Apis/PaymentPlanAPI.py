
import logging

import utils

from webapp2 import Route

from base import ShingHandler

from Models.ModelPaymentPlan import PaymentPlan


class PaymentPlanAPI(ShingHandler):
	"""docstring for PaymentPlanAPI"""

	def create(self):
		name = self.request.get('name')
		grace_period = self.request.get_range('grace_period')
		subscription_period = self.request.get_range('subscription_period')
		logging.info("Creating payment plan %s" % name)
		if all([name, grace_period, subscription_period]):
			name = utils.to_upper(name)
			PaymentPlan.create(name=name, grace_period=grace_period, subscription_period=subscription_period)
		else:
			print "missing mandatory field"


payment_plan_api = [
    Route('/api/payment/create', handler=PaymentPlanAPI, handler_method="create", methods=["POST"]),
    ]