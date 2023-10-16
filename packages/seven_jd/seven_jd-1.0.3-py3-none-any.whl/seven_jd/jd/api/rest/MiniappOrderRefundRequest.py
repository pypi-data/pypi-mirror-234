from seven_jd.jd.api.base import RestApi

class MiniappOrderRefundRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.openId = None
			self.refundAmount = None
			self.refundUuid = None
			self.orderId = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.miniapp.order.refund'

			





