from seven_jd.jd.api.base import RestApi

class SellerCouponWriteLockCouponRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.port = None
			self.requestId = None
			self.time = None
			self.purpose = None
			self.operateTime = None
			self.couponId = None

		def getapiname(self):
			return 'jingdong.seller.coupon.write.lockCoupon'

			





