from seven_jd.jd.api.base import RestApi

class MiniappCiserviceQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.uuid = None
			self.token = None

		def getapiname(self):
			return 'jingdong.miniapp.ciservice.query'

			





