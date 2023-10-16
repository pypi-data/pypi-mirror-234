from seven_jd.jd.api.base import RestApi

class PopAfsSoaRefundapplyQueryPageListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ids = None
			self.status = None
			self.orderId = None
			self.buyerId = None
			self.buyerName = None
			self.applyTimeStart = None
			self.applyTimeEnd = None
			self.checkTimeStart = None
			self.checkTimeEnd = None
			self.pageIndex = None
			self.pageSize = None
			self.storeId = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.pop.afs.soa.refundapply.queryPageList'

			





