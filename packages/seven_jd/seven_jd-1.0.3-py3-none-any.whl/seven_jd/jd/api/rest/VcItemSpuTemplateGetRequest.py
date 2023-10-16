from seven_jd.jd.api.base import RestApi

class VcItemSpuTemplateGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.cid3 = None
			self.brand_id = None
			self.model = None

		def getapiname(self):
			return 'jingdong.vc.item.spuTemplate.get'

			





