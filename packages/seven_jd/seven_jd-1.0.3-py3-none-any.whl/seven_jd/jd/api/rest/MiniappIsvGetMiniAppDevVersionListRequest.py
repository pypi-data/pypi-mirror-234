from seven_jd.jd.api.base import RestApi

class MiniappIsvGetMiniAppDevVersionListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.miniAppId = None
			self.IsvAppId = None

		def getapiname(self):
			return 'jingdong.miniapp.isv.getMiniAppDevVersionList'

			





