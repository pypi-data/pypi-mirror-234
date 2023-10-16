from seven_jd.jd.api.base import RestApi

class CarMemberSkuQueryCarBSkuListByShopIdRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.param = None

		def getapiname(self):
			return 'jingdong.car.member.sku.queryCarBSkuListByShopId'

			
	

class Param(object):
		def __init__(self):
			"""
			"""
			self.jdCarIds = None
			self.pageSize = None
			self.cid2 = None
			self.page = None
			self.cid3 = None
			self.cid1 = None
			self.shopId = None





