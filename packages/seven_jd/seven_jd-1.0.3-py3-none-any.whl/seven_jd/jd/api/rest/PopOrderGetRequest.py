from seven_jd.jd.api.base import RestApi

class PopOrderGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.order_state = None
			self.optional_fields = None
			self.order_id = None

		def getapiname(self):
			return 'jingdong.pop.order.get'

			





