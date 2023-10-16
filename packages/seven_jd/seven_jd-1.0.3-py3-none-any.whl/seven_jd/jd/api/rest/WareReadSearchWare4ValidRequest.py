from seven_jd.jd.api.base import RestApi

class WareReadSearchWare4ValidRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.wareId = None
			self.searchKey = None
			self.searchField = None
			self.categoryId = None
			self.shopCategoryIdLevel1 = None
			self.shopCategoryIdLevel2 = None
			self.templateId = None
			self.promiseId = None
			self.brandId = None
			self.featureKey = None
			self.featureValue = None
			self.wareStatusValue = None
			self.itemNum = None
			self.barCode = None
			self.colType = None
			self.startCreatedTime = None
			self.endCreatedTime = None
			self.startJdPrice = None
			self.endJdPrice = None
			self.startOnlineTime = None
			self.endOnlineTime = None
			self.startModifiedTime = None
			self.endModifiedTime = None
			self.startOfflineTime = None
			self.endOfflineTime = None
			self.startStockNum = None
			self.endStockNum = None
			self.orderField = None
			self.orderType = None
			self.pageNo = None
			self.pageSize = None
			self.transportId = None
			self.claim = None
			self.groupId = None
			self.multiCategoryId = None
			self.warePropKey = None
			self.warePropValue = None
			self.field = None

		def getapiname(self):
			return 'jingdong.ware.read.searchWare4Valid'

			





