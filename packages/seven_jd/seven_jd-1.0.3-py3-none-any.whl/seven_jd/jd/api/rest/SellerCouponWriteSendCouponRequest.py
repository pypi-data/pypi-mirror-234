from seven_jd.jd.api.base import RestApi

class SellerCouponWriteSendCouponRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ip = None
			self.deployAppName = None
			self.port = None
			self.userPin = None
			self.putKey = None
			self.requestId = None
			self.requestRetry = None

		def getapiname(self):
			return 'jingdong.seller.coupon.write.sendCoupon'

			





