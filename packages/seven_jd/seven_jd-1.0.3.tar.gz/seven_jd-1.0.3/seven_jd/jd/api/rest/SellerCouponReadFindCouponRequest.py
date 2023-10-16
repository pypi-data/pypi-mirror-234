from seven_jd.jd.api.base import RestApi

class SellerCouponReadFindCouponRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ip = None
			self.deployAppName = None
			self.port = None
			self.putKey = None

		def getapiname(self):
			return 'jingdong.seller.coupon.read.findCoupon'

			





