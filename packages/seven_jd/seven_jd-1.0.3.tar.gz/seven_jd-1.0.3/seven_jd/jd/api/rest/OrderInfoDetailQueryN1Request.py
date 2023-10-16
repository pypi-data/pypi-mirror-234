from seven_jd.jd.api.base import RestApi

class OrderInfoDetailQueryN1Request(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.activityId = None
			self.startRow = None
			self.venderId = None
			self.searchDate = None
			self.endRow = None

		def getapiname(self):
			return 'jingdong.orderInfoDetailQuery.n1'

			





