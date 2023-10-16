from seven_jd.jd.api.base import RestApi

class GroupMarketQueryChatGroupsRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.Language = None
			self.appName = None
			self.channel = None
			self.userPin = None
			self.actName = None
			self.status = None
			self.actStartTime = None
			self.actEndTime = None
			self.page = None
			self.pageSize = None

		def getapiname(self):
			return 'jingdong.groupMarket.queryChatGroups'

			





