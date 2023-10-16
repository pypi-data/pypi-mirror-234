from seven_jd.jd.api.base import RestApi

class MarketToolCouponApiServiceCouponReadOuterServiceQueryCouponPageRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.creator = None
			self.newStatus = None
			self.skuIdStr = None
			self.bindType = None
			self.pageSize = None
			self.couponId = None
			self.wareChoseType = None
			self.delete = None
			self.spuId = None
			self.page = None
			self.beginTime = None
			self.endTime = None
			self.skuId = None
			self.couponTitle = None
			self.couponIdStr = None
			self.appName = None
			self.ip = None
			self.appId = None

		def getapiname(self):
			return 'jingdong.market.tool.coupon.api.service.CouponReadOuterService.queryCouponPage'

			





