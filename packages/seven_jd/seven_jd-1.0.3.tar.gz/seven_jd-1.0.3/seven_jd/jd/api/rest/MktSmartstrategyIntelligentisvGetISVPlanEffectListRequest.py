from seven_jd.jd.api.base import RestApi

class MktSmartstrategyIntelligentisvGetISVPlanEffectListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.pageNo = None
			self.pageSize = None

		def getapiname(self):
			return 'jingdong.mkt.smartstrategy.intelligentisv.getISVPlanEffectList'

			





