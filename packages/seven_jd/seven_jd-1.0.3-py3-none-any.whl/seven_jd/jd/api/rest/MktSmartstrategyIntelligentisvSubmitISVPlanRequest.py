from seven_jd.jd.api.base import RestApi

class MktSmartstrategyIntelligentisvSubmitISVPlanRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.targetThirdCateIds = None
			self.planName = None
			self.targetSecondCateIds = None
			self.targetFirstCateIds = None
			self.multiChannels = None
			self.pin = None
			self.pullNewer = None
			self.planBeginTime = None
			self.repurchase = None
			self.putKey = None
			self.catePopStrategy = None
			self.planEndTime = None
			self.campus = None

		def getapiname(self):
			return 'jingdong.mkt.smartstrategy.intelligentisv.submitISVPlan'

			





