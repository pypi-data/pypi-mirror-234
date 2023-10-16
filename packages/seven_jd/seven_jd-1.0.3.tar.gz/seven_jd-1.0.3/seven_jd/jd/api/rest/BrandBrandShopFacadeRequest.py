from seven_jd.jd.api.base import RestApi

class BrandBrandShopFacadeRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.number = None
			self.size = None
			self.bId = None

		def getapiname(self):
			return 'jingdong.brand.BrandShopFacade'

			





