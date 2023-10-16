from seven_jd.jd.api.base import RestApi

class ShorturlGenerateURLRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.url = None

		def getapiname(self):
			return 'jingdong.shorturl.generateURL'

			





