from seven_jd.jd.api.base import RestApi

class SelfOperationShopSearchApiServiceSearchRecomJsfServiceCheckHotWordRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.hotWord = None

		def getapiname(self):
			return 'jingdong.self.operation.shop.search.api.service.SearchRecomJsfService.checkHotWord'

			





