from seven_jd.jd.api.base import RestApi

class QueryCid3ListByShopId2Request(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.param1 = None

		def getapiname(self):
			return 'jingdong.queryCid3ListByShopId2'

			
	

class Param1(object):
		def __init__(self):
			"""
			"""
			self.jdCarIds = None
			self.pageSize = None
			self.cid2 = None
			self.page = None
			self.cid3 = None
			self.shopId = None
			self.cid1 = None





