from seven_jd.jd.api.base import RestApi

class PopOrderEnSearchRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.start_date = None
			self.end_date = None
			self.order_state = None
			self.optional_fields = None
			self.page = None
			self.page_size = None
			self.sortType = None
			self.dateType = None

		def getapiname(self):
			return 'jingdong.pop.order.enSearch'

			





