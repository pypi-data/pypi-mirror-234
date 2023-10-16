from seven_jd.jd.api.base import RestApi

class InteractCenterApiServiceReadGetOtherCouponInfoRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appName = None
			self.appId = None
			self.channel = None
			self.batchKey = None
			self.activityEndTime = None
			self.prizeType = None
			self.activityStartTime = None

		def getapiname(self):
			return 'jingdong.interact.center.api.service.read.getOtherCouponInfo'

			





