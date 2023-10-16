from seven_jd.jd.api.base import RestApi

class PromoUnitGetVenderIsvActivityRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.pluginName = None
			self.pageSize = None
			self.pageNo = None

		def getapiname(self):
			return 'jingdong.promo.unit.getVenderIsvActivity'

			





