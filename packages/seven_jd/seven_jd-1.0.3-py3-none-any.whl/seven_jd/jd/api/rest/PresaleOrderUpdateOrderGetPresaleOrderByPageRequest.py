from seven_jd.jd.api.base import RestApi

class PresaleOrderUpdateOrderGetPresaleOrderByPageRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.userPin = None
			self.orderId = None
			self.orderStatusItem = None
			self.startTime = None
			self.endTime = None
			self.skuID = None
			self.beginIndex = None
			self.endIndex = None

		def getapiname(self):
			return 'jingdong.presale.order.updateOrder.getPresaleOrderByPage'

			





