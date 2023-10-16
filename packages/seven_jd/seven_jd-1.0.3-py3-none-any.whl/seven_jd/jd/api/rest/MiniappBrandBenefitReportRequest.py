from seven_jd.jd.api.base import RestApi

class MiniappBrandBenefitReportRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.benId = None
			self.benState = None
			self.openId = None
			self.benType = None
			self.benNo = None
			self.reportTime = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.miniapp.brand.benefit.report'

			





