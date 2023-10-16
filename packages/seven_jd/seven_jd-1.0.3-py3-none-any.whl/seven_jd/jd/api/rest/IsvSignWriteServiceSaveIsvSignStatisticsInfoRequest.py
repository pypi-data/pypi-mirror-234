from seven_jd.jd.api.base import RestApi

class IsvSignWriteServiceSaveIsvSignStatisticsInfoRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.activityId = None
			self.pin = None
			self.totalSignCount = None
			self.venderId = None
			self.lastedSignedTime = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.IsvSignWriteService.saveIsvSignStatisticsInfo'

			





