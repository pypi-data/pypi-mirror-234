from seven_jd.jd.api.base import RestApi

class OrderInfoDetailQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.activityId = None
			self.searchDate = None
			self.venderId = None
			self.startRow = None
			self.endRow = None

		def getapiname(self):
			return 'jingdong.orderInfoDetailQuery'

			





