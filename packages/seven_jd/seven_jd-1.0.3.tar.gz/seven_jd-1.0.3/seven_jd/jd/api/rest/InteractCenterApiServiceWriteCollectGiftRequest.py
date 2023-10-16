from seven_jd.jd.api.base import RestApi

class InteractCenterApiServiceWriteCollectGiftRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appName = None
			self.channel = None
			self.pin = None
			self.isEverydayAward = None
			self.activityId = None
			self.ip = None
			self.type = None
			self.rfId = None
			self.source = None

		def getapiname(self):
			return 'jingdong.interact.center.api.service.write.collectGift'

			





