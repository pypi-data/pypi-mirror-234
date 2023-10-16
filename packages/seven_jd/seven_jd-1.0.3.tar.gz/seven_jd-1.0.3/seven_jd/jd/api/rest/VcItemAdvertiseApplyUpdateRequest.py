from seven_jd.jd.api.base import RestApi

class VcItemAdvertiseApplyUpdateRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.sku_id = None
			self.ad_word = None
			self.apply_id = None

		def getapiname(self):
			return 'jingdong.vc.item.advertise.apply.update'

			





