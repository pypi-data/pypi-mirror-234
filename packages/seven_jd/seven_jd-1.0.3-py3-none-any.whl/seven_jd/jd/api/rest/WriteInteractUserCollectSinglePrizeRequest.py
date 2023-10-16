from seven_jd.jd.api.base import RestApi

class WriteInteractUserCollectSinglePrizeRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appName = None
			self.appId = None
			self.clientChannel = None
			self.activityId = None
			self.userPin = None
			self.prizeRuleId = None
			self.businessId = None
			self.type = None
			self.channel = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.write.interact.user.collectSinglePrize'

			





