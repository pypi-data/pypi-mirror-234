from seven_jd.jd.api.base import RestApi

class SelfOperationShopSearchApiServiceSearchRecomJsfServiceGetSearchRecomListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.venderId = None

		def getapiname(self):
			return 'jingdong.self.operation.shop.search.api.service.SearchRecomJsfService.getSearchRecomList'

			





