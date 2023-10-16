from seven_jd.jd.api.base import RestApi

class GroupMarketJoinGroupRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.Language = None
			self.appName = None
			self.channel = None
			self.pin = None
			self.groupId = None
			self.nickname = None
			self.id = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.groupMarket.joinGroup'

			





