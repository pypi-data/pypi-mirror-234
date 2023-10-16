from seven_jd.jd.api.base import RestApi

class VcItemPrimaryPicAppliesFindRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ware_id = None
			self.name = None
			self.brand_id = None
			self.category_id = None
			self.state = None
			self.begin_apply_time = None
			self.end_apply_time = None
			self.page = None
			self.length = None

		def getapiname(self):
			return 'jingdong.vc.item.primaryPic.applies.find'

			





