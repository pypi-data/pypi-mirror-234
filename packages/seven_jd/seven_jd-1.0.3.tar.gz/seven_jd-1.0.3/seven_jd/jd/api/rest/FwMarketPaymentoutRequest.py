from seven_jd.jd.api.base import RestApi

class FwMarketPaymentoutRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.requestNo = None
			self.activityId = None
			self.appId = None
			self.price = None
			self.isMainService = None
			self.serviceCycle = None
			self.skuId = None
			self.serviceCode = None
			self.orderNum = None
			self.itemCode = None
			self.outOrderId = None
			self.value1 = None
			self.resultPageType = None
			self.successUrl = None
			self.ip = None

		def getapiname(self):
			return 'jingdong.fw.market.paymentout'

			





