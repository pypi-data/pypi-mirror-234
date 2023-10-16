from seven_jd.jd.api.base import RestApi

class EptOrderGetorderinfobyidRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.orderId = None

		def getapiname(self):
			return 'jingdong.ept.order.getorderinfobyid'

			





