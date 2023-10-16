from seven_jd.jd.api.base import RestApi

class VcAplsStockUpdateProdStockInfoRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.vendorCode = None
			self.companyId = None
			self.stockRfId = None
			self.skuid = None
			self.stockNum = None

		def getapiname(self):
			return 'jingdong.vc.apls.stock.updateProdStockInfo'

			





