from seven_jd.jd.api.base import RestApi

class EptVenderBrandGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.status = None
			self.pageSize = None
			self.currentPage = None

		def getapiname(self):
			return 'jingdong.ept.vender.brand.get'

			





