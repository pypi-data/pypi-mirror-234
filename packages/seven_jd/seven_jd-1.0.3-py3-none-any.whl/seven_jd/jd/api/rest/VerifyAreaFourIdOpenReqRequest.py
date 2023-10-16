from seven_jd.jd.api.base import RestApi

class VerifyAreaFourIdOpenReqRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.countyId = None
			self.cityId = None
			self.townId = None
			self.provinceId = None

		def getapiname(self):
			return 'jingdong.verifyAreaFourIdOpenReq'

			





