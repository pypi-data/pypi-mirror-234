from seven_jd.jd.api.base import RestApi

class MiniappIsvGetDevopsPackIdByRequestUuidRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.miniAppId = None
			self.uuid = None

		def getapiname(self):
			return 'jingdong.miniapp.isv.getDevopsPackIdByRequestUuid'

			





