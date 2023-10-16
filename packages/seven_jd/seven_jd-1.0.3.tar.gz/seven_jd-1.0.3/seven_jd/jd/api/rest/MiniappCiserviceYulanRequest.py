from seven_jd.jd.api.base import RestApi

class MiniappCiserviceYulanRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.packId = None
			self.token = None

		def getapiname(self):
			return 'jingdong.miniapp.ciservice.yulan'

			





