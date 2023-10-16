from seven_jd.jd.api.base import RestApi

class StockWriteUpdateSkuStockRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.skuId = None
			self.stockNum = None
			self.storeId = None

		def getapiname(self):
			return 'jingdong.stock.write.updateSkuStock'

			





