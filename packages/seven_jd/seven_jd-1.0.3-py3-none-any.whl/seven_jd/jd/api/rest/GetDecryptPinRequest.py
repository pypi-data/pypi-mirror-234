from seven_jd.jd.api.base import RestApi

class GetDecryptPinRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.userPin = None
			self.appName = None
			self.appId = None
			self.requestIP = None
			self.time = None
			self.koiKey = None
			self.encryptPin = None

		def getapiname(self):
			return 'jingdong.getDecryptPin'

			





