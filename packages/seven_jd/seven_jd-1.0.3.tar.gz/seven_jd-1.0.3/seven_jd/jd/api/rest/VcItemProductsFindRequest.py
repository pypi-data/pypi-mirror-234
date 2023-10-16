from seven_jd.jd.api.base import RestApi

class VcItemProductsFindRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ware_id = None
			self.name = None
			self.brand_id = None
			self.category_id = None
			self.sale_state = None
			self.begin_modify_time = None
			self.end_modify_time = None
			self.offset = None
			self.page_size = None

		def getapiname(self):
			return 'jingdong.vc.item.products.find'

			





