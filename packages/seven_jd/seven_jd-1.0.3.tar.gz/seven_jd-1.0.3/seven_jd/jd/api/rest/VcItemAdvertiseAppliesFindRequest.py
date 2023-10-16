from seven_jd.jd.api.base import RestApi

class VcItemAdvertiseAppliesFindRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ware_id = None
			self.category = None
			self.product_name = None
			self.brand_id = None
			self.begin_apply_time = None
			self.end_apply_time = None
			self.state = None
			self.offset = None
			self.page_size = None

		def getapiname(self):
			return 'jingdong.vc.item.advertise.applies.find'

			





