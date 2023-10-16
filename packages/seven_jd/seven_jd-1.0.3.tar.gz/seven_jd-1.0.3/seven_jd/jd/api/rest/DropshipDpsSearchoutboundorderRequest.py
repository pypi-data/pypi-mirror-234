from seven_jd.jd.api.base import RestApi

class DropshipDpsSearchoutboundorderRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.pageSize = None
			self.page = None
			self.beginDate = None
			self.endDate = None
			self.modifiedBeginDate = None
			self.modifiedEndDate = None

		def getapiname(self):
			return 'jingdong.dropship.dps.searchoutboundorder'

			





