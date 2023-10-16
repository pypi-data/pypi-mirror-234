from seven_jd.jd.api.base import RestApi

class MiniappIsvCommitMiniAppDevVersionRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.IsvAppId = None
			self.appId = None
			self.packageId = None
			self.description = None
			self.versionName = None

		def getapiname(self):
			return 'jingdong.miniapp.isv.commitMiniAppDevVersion'

			





