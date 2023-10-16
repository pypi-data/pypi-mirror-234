from seven_jd.jd.api.base import RestApi

class VcItemProductAppliesFindRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ware_id = None
			self.ware_name = None
			self.state = None
			self.begin_time = None
			self.end_time = None
			self.page = None
			self.length = None

		def getapiname(self):
			return 'jingdong.vc.item.product.applies.find'

			





