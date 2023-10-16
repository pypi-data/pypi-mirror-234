from seven_jd.jd.api.base import RestApi

class SkuReadSearchSkuListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.wareId = None
			self.skuId = None
			self.skuStatuValue = None
			self.maxStockNum = None
			self.minStockNum = None
			self.endCreatedTime = None
			self.endModifiedTime = None
			self.startCreatedTime = None
			self.startModifiedTime = None
			self.outId = None
			self.colType = None
			self.itemNum = None
			self.wareTitle = None
			self.orderFiled = None
			self.orderType = None
			self.pageNo = None
			self.page_size = None
			self.valid = None
			self.key = None
			self.value = None
			self.cn = None
			self.field = None

		def getapiname(self):
			return 'jingdong.sku.read.searchSkuList'

			





