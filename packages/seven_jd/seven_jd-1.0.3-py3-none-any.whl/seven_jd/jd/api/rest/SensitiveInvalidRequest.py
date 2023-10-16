from seven_jd.jd.api.base import RestApi

class SensitiveInvalidRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.secretKey = None
			self.words = None
			self.source = None
			self.time = None

		def getapiname(self):
			return 'jingdong.sensitive.invalid'

			





