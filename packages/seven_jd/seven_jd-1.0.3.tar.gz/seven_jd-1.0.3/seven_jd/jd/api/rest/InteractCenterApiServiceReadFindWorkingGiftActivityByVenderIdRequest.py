from seven_jd.jd.api.base import RestApi

class InteractCenterApiServiceReadFindWorkingGiftActivityByVenderIdRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appName = None
			self.appId = None
			self.channel = None
			self.type = None

		def getapiname(self):
			return 'jingdong.interact.center.api.service.read.findWorkingGiftActivityByVenderId'

			





