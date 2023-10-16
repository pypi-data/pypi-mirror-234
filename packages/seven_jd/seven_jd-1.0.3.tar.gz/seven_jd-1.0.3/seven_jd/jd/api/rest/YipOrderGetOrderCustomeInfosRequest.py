from seven_jd.jd.api.base import RestApi

class YipOrderGetOrderCustomeInfosRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.orderId = None
			self.subSkuId = None
			self.appId = None
			self.source = None
			self.customFields = None
			self.skuId = None

		def getapiname(self):
			return 'jingdong.yip.order.getOrderCustomeInfos'

			





