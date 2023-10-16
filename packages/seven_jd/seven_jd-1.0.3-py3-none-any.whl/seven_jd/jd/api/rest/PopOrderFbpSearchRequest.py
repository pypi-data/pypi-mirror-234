from seven_jd.jd.api.base import RestApi

class PopOrderFbpSearchRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.startDate = None
			self.endDate = None
			self.orderState = None
			self.page = None
			self.pageSize = None
			self.colType = None
			self.optionalFields = None
			self.orderId = None
			self.sortType = None
			self.dateType = None
			self.storeId = None
			self.cky2 = None

		def getapiname(self):
			return 'jingdong.pop.order.fbp.search'

			





