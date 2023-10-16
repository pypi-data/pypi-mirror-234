from seven_jd.jd.api.base import RestApi

class SellerCouponWritePushCouponRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.port = None
			self.requestId = None
			self.pin = None
			self.distrTime = None
			self.couponId = None
			self.uuid = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.seller.coupon.write.pushCoupon'

			





