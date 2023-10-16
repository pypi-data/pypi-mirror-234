from seven_jd.jd.api.base import RestApi

class GroupMarketGetMemberInfoRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.Language = None
			self.appName = None
			self.channel = None
			self.gid = None
			self.pinList = None
			self.id = None
			self.queryIsMember = None

		def getapiname(self):
			return 'jingdong.groupMarket.getMemberInfo'

			





