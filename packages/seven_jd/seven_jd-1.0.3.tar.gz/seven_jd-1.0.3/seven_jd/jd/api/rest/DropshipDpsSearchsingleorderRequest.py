from seven_jd.jd.api.base import RestApi

class DropshipDpsSearchsingleorderRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.customOrderId = None

		def getapiname(self):
			return 'jingdong.dropship.dps.searchsingleorder'

			





