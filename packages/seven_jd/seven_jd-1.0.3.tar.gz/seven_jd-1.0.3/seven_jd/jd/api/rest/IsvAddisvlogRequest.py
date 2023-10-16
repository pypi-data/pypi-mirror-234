from seven_jd.jd.api.base import RestApi

class IsvAddisvlogRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.account = None
			self.clientIp = None
			self.operationTime = None
			self.operationContent = None
			self.useIsvAppkey = None
			self.reqjosUrl = None
			self.touchNumber = None
			self.touchFiles = None

		def getapiname(self):
			return 'jingdong.isv.addisvlog'

			





