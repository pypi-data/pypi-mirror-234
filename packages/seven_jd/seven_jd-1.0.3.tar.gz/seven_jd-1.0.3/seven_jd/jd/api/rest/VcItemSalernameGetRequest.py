from seven_jd.jd.api.base import RestApi

class VcItemSalernameGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.saler_code = None

		def getapiname(self):
			return 'jingdong.vc.item.salername.get'

			





