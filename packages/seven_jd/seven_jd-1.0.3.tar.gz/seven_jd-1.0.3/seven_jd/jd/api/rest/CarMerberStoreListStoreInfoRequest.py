from seven_jd.jd.api.base import RestApi

class CarMerberStoreListStoreInfoRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.storeMakeId = None
			self.distance = None
			self.pageNo = None
			self.pageSize = None
			self.lon = None
			self.sort = None
			self.lat = None
			self.platform = None
			self.storeLabelId = None

		def getapiname(self):
			return 'jingdong.car.merber.store.listStoreInfo'

			





