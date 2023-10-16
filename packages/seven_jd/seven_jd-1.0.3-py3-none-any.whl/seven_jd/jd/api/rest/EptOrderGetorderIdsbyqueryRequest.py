from seven_jd.jd.api.base import RestApi

class EptOrderGetorderIdsbyqueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.orderStatus = None
			self.locked = None
			self.disputed = None
			self.bookTimeBegin = None
			self.bookTimeEnd = None
			self.userPin = None
			self.startRow = None

		def getapiname(self):
			return 'jingdong.ept.order.getorderIdsbyquery'

			





