from seven_jd.jd.api.base import RestApi

class UserRelatedRpcI18nServiceGetOpenIdRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.pin = None

		def getapiname(self):
			return 'jingdong.UserRelatedRpcI18nService.getOpenId'

			





