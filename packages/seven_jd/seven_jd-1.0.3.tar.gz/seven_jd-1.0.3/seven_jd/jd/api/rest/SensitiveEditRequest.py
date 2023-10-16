from seven_jd.jd.api.base import RestApi

class SensitiveEditRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.secretKey = None
			self.g = None
			self.cat = None
			self.contextWhite = None
			self.vendor = None
			self.brand = None
			self.extendMap = None
			self.source = None
			self.time = None
			self.word = None

		def getapiname(self):
			return 'jingdong.sensitive.edit'

			





