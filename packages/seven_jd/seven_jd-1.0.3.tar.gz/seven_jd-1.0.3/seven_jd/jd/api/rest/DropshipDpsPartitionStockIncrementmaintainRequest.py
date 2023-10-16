from seven_jd.jd.api.base import RestApi

class DropshipDpsPartitionStockIncrementmaintainRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.sku = None
			self.stockNum = None
			self.storeId = None
			self.rfId = None

		def getapiname(self):
			return 'jingdong.dropship.dps.partitionStock.incrementmaintain'

			





