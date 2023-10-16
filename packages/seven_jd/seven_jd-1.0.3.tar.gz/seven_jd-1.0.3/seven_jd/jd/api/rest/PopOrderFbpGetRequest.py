from seven_jd.jd.api.base import RestApi

class PopOrderFbpGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.orderState = None
			self.colType = None
			self.optionalFields = None
			self.orderId = None

		def getapiname(self):
			return 'jingdong.pop.order.fbp.get'

			





