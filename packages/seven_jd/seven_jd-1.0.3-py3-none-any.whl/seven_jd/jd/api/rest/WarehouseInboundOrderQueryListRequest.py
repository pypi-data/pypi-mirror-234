from seven_jd.jd.api.base import RestApi

class WarehouseInboundOrderQueryListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.pageIndex = None
			self.pageSize = None
			self.createTimeBegin = None
			self.createTimeEnd = None
			self.unpackingTimeBegin = None
			self.unpackingTimeEnd = None
			self.remark1 = None
			self.remark2 = None
			self.remark3 = None
			self.remark4 = None
			self.remark5 = None

		def getapiname(self):
			return 'jingdong.warehouse.inbound.order.query.list'

			





