from seven_jd.jd.api.base import RestApi

class MiniappRefundRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.userId = None
			self.refundUuid = None
			self.isHalfRefund = None
			self.orderId = None
			self.refundAmount = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.miniapp.refund'

			





