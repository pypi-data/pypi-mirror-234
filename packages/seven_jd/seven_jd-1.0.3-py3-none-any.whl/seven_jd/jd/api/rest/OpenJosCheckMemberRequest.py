from seven_jd.jd.api.base import RestApi

class OpenJosCheckMemberRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appId = None
			self.userName = None
			self.memberId = None
			self.open_id_buyer = None

		def getapiname(self):
			return 'jingdong.openJos.checkMember'

			





