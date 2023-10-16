from seven_jd.jd.api.base import RestApi

class SellerCouponWriteCreateRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ip = None
			self.port = None
			self.name = None
			self.type = None
			self.bindType = None
			self.grantType = None
			self.num = None
			self.discount = None
			self.quota = None
			self.validityType = None
			self.days = None
			self.beginTime = None
			self.endTime = None
			self.password = None
			self.batchKey = None
			self.member = None
			self.takeBeginTime = None
			self.takeEndTime = None
			self.takeRule = None
			self.takeNum = None
			self.display = None
			self.platformType = None
			self.platform = None
			self.shareType = None
			self.activityLink = None
			self.userClass = None
			self.paidMembers = None
			self.numPerSending = None
			self.skuId = None

		def getapiname(self):
			return 'jingdong.seller.coupon.write.create'

			





