from seven_jd.jd.api.base import RestApi

class EdiInventorySendRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.vendorCode = None
			self.vendorName = None
			self.vendorProductId = None
			self.inventoryDate = None
			self.totalQuantity = None
			self.estimateDate = None
			self.totalEstimateQuantity = None
			self.costPrice = None
			self.storeId = None
			self.storeName = None
			self.quantity = None
			self.estimateQuantity = None

		def getapiname(self):
			return 'jingdong.edi.inventory.send'

			





