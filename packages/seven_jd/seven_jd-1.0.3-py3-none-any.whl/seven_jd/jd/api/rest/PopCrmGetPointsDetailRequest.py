from seven_jd.jd.api.base import RestApi

class PopCrmGetPointsDetailRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.customerPin = None
			self.startTime = None
			self.endTime = None
			self.startPage = None
			self.endPage = None
			self.page = None
			self.pageSize = None
			self.startRowKey = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.pop.crm.getPointsDetail'

			





