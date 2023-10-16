from seven_jd.jd.api.base import RestApi

class ShorturlGenerateURLFastestRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.domain = None
			self.length = None
			self.realUrl = None
			self.expiredDays = None

		def getapiname(self):
			return 'jingdong.shorturl.generateURLFastest'

			





