from seven_jd.jd.api.base import RestApi

class GetUserEntryWechatGroupTrackRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.traceId = None
			self.opIp = None
			self.businessType = None
			self.jdPin = None

		def getapiname(self):
			return 'jingdong.getUserEntryWechatGroupTrack'

			





