from seven_jd.jd.api.base import RestApi

class TokenToPinCenterConverstionJmEncryptPinRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.encryptPin = None
			self.appKey = None

		def getapiname(self):
			return 'jingdong.TokenToPinCenter.converstionJmEncryptPin'

			





