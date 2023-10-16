from seven_jd.jd.api.base import RestApi

class WareProductUpdateQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.sku_status = None
			self.start_SaleDate = None
			self.end_SaleDate = None
			self.thirdCid = None
			self.scrollId = None

		def getapiname(self):
			return 'jingdong.ware.product.update.query'

			





