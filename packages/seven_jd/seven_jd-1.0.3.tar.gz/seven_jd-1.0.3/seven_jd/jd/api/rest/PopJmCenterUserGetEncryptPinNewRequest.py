from seven_jd.jd.api.base import RestApi

class PopJmCenterUserGetEncryptPinNewRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.source = None
			self.token = None

		def getapiname(self):
			return 'jingdong.pop.jm.center.user.getEncryptPinNew'

			





