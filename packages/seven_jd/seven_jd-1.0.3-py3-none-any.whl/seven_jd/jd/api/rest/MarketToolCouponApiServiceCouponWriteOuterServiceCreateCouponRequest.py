from seven_jd.jd.api.base import RestApi

class MarketToolCouponApiServiceCouponWriteOuterServiceCreateCouponRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.wareGrade = None
			self.num = None
			self.discount = None
			self.strategyParam = None
			self.type = None
			self.skuIdList = None
			self.couponId = None
			self.shareType = None
			self.storeId = None
			self.takeEndTime = None
			self.high = None
			self.takeNum = None
			self.quota = None
			self.officialType = None
			self.beginTime = None
			self.promoteChannel = None
			self.remainNum = None
			self.storeType = None
			self.display = None
			self.busiCode = None
			self.wareChoseType = None
			self.userClass = None
			self.userLevel = None
			self.takeBeginTime = None
			self.validityType = None
			self.takeRule = None
			self.hourCoupon = None
			self.name = None
			self.activityLink = None
			self.days = None
			self.style = None
			self.endTime = None
			self.adWord = None
			self.spuIdList = None
			self.channels = None
			self.channelSelectType = None
			self.selectType = None
			self.platforms = None
			self.appName = None
			self.ip = None
			self.appId = None

		def getapiname(self):
			return 'jingdong.market.tool.coupon.api.service.CouponWriteOuterService.createCoupon'

			





