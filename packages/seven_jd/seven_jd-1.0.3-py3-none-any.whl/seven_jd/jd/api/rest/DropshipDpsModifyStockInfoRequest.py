from seven_jd.jd.api.base import RestApi

class DropshipDpsModifyStockInfoRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.sku = None
			self.stockNum = None

		def getapiname(self):
			return 'jingdong.dropship.dps.modifyStockInfo'

			





