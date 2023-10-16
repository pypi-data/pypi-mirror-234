from seven_jd.jd.api.base import RestApi

class InteractCenterApiServiceWriteCloseGiftActivityRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appName = None
			self.channel = None
			self.activityId = None
			self.type = None

		def getapiname(self):
			return 'jingdong.interact.center.api.service.write.closeGiftActivity'

			





