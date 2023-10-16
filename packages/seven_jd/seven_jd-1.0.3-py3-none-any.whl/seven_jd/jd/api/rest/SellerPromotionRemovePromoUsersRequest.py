from seven_jd.jd.api.base import RestApi

class SellerPromotionRemovePromoUsersRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ip = None
			self.port = None
			self.request_id = None
			self.promoId = None
			self.pin = None
			self.beginTime = None
			self.endTime = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.seller.promotion.removePromoUsers'

			





