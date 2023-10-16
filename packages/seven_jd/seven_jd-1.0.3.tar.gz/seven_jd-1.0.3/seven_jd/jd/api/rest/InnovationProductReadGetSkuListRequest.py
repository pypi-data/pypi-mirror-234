from seven_jd.jd.api.base import RestApi

class InnovationProductReadGetSkuListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.spuId = None
			self.skuId = None
			self.pageNo = None
			self.pageSize = None
			self.categoryId = None
			self.title = None

		def getapiname(self):
			return 'jingdong.innovation.product.read.getSkuList'

			





