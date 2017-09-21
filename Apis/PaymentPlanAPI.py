
from webapp2 import Route

from base import ShingHandler

payment_plan_api = [
    Route('/api/payment/create', handler=PaymentPlan, handler_method="create", methods=["POST"]),
    ]

class PaymentPlan(ShingHandler):
	"""docstring for PaymentPlan"""

	def create(self):
		pass
