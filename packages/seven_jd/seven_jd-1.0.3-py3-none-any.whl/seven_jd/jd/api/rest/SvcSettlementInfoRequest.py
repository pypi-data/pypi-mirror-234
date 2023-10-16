from seven_jd.jd.api.base import RestApi

class SvcSettlementInfoRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appId = None
			self.page = None
			self.createTimeEnd = None
			self.clientIp = None
			self.createTimeBegin = None
			self.size = None

		def getapiname(self):
			return 'jingdong.svc.settlement.info'

			





