from seven_jd.jd.api.base import RestApi

class MiniappOrderCancelRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.openId = None
			self.orderId = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.miniapp.order.cancel'

			





