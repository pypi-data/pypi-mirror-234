from seven_jd.jd.api.base import RestApi

class MiniappCardNoRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.credentialsNo = None
			self.userId = None
			self.name = None
			self.type = None

		def getapiname(self):
			return 'jingdong.miniapp.cardNo'

			





