from seven_jd.jd.api.base import RestApi

class GroupMarketCreateActivityRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.Language = None
			self.appName = None
			self.channel = None
			self.offerReceiveType = None
			self.autoSendTxt = None
			self.actEndTime = None
			self.attribute1 = None
			self.actName = None
			self.actStartTime = None
			self.attribute2 = None
			self.prepareTime = None
			self.id = None
			self.actImg = None
			self.actLink = None

		def getapiname(self):
			return 'jingdong.groupMarket.createActivity'

			





