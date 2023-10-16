from seven_jd.jd.api.base import RestApi

class JmOrderGetPayUrlRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.serviceCode = None
			self.accessCode = None
			self.orderNum = None
			self.skuId = None
			self.clientIp = None

		def getapiname(self):
			return 'jingdong.jm.order.getPayUrl'

			





