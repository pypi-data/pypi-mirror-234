from seven_jd.jd.api.base import RestApi

class VcItemPrimaryPicCreateRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.sku_id = None
			self.image_list = None
			self.sku_id_long = None
			self.image_list_long = None
			self.sku_id_lucency = None
			self.image_list_lucency = None
			self.is_publishSchedule = None
			self.publish_time = None

		def getapiname(self):
			return 'jingdong.vc.item.primaryPic.create'

			





