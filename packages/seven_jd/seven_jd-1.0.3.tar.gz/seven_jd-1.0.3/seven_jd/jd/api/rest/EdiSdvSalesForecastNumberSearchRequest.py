from seven_jd.jd.api.base import RestApi

class EdiSdvSalesForecastNumberSearchRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.page = None
			self.pageSize = None

		def getapiname(self):
			return 'jingdong.edi.sdv.sales.forecast.number.search'

			





