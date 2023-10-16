from seven_jd.jd.api.base import RestApi

class SellerPromotionV2GetPromoLimitRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ip = None
			self.port = None
			self.category_id = None
			self.start_time = None
			self.end_time = None

		def getapiname(self):
			return 'jingdong.seller.promotion.v2.getPromoLimit'

			





