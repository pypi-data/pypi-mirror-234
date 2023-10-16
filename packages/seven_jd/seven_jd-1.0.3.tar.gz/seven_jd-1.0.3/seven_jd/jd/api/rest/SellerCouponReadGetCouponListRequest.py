from seven_jd.jd.api.base import RestApi

class SellerCouponReadGetCouponListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ip = None
			self.port = None
			self.couponId = None
			self.type = None
			self.grantType = None
			self.bindType = None
			self.grantWay = None
			self.name = None
			self.createMonth = None
			self.creatorType = None
			self.closed = None
			self.page = None
			self.pageSize = None

		def getapiname(self):
			return 'jingdong.seller.coupon.read.getCouponList'

			





