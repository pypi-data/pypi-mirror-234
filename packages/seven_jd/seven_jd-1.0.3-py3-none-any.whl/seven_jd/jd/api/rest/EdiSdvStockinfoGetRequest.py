from seven_jd.jd.api.base import RestApi

class EdiSdvStockinfoGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.recordDate = None
			self.pageNum = None
			self.pageSize = None

		def getapiname(self):
			return 'jingdong.edi.sdv.stockinfo.get'

			





