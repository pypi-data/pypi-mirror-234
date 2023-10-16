from seven_jd.jd.api.base import RestApi

class MarketServiceListGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.page_size = None
			self.page = None
			self.service_status = None
			self.start_date = None
			self.end_date = None

		def getapiname(self):
			return 'jingdong.market.service.list.get'

			





