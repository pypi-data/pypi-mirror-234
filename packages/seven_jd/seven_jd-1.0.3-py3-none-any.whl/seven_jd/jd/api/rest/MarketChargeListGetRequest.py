from seven_jd.jd.api.base import RestApi

class MarketChargeListGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.service_code = None
			self.service_id = None

		def getapiname(self):
			return 'jingdong.market.charge.list.get'

			





