from seven_jd.jd.api.base import RestApi

class GroupMarketQueryGroupByClusterIdRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.Language = None
			self.appName = None
			self.channel = None
			self.id = None

		def getapiname(self):
			return 'jingdong.groupMarket.queryGroupByClusterId'

			





