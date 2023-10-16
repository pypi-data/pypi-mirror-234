from seven_jd.jd.api.base import RestApi

class MarketToolCouponApiServiceCouponWriteOuterServiceCloseCouponRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.couponId = None
			self.appName = None
			self.ip = None
			self.appId = None

		def getapiname(self):
			return 'jingdong.market.tool.coupon.api.service.CouponWriteOuterService.closeCoupon'

			





