from seven_jd.jd.api.base import RestApi

class PromoUnitCloseIsvSignActivityRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appName = None
			self.appKey = None
			self.id = None

		def getapiname(self):
			return 'jingdong.promo.unit.closeIsvSignActivity'

			





