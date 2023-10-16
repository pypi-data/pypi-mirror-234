from seven_jd.jd.api.base import RestApi

class JosServiceWriteVenderJosShopGiftWriteServiceCloseActivityRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appName = None
			self.channel = None
			self.activityId = None
			self.activityType = None

		def getapiname(self):
			return 'jingdong.jos.service.write.vender.JosShopGiftWriteService.closeActivity'

			





