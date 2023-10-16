from seven_jd.jd.api.base import RestApi

class SellerPromotionV2ListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ip = None
			self.port = None
			self.promo_id = None
			self.name = None
			self.type = None
			self.favor_mode = None
			self.begin_time = None
			self.end_time = None
			self.promo_status = None
			self.ware_id = None
			self.sku_id = None
			self.page = None
			self.pageS_size = None
			self.src_type = None
			self.start_id = None

		def getapiname(self):
			return 'jingdong.seller.promotion.v2.list'

			





