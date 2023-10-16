from seven_jd.jd.api.base import RestApi

class UstFlowDataStatisticOnlineRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.tm = None
			self.tmCycle = None
			self.activeId = None

		def getapiname(self):
			return 'jingdong.ustFlowDataStatisticOnline'

			





