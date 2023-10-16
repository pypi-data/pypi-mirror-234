from seven_jd.jd.api.base import RestApi

class PromoUnitAddIsvActivityRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.note = None
			self.shared = None
			self.callBackUrl = None
			self.channelType = None
			self.source = None
			self.pluginName = None
			self.imageUrl = None
			self.ruleType = None
			self.name = None
			self.id = None
			self.beginTime = None
			self.endTime = None
			self.isvUrl = None
			self.categoryId = None
			self.status = None
			self.appropriateCrowd = None
			self.priority = None
			self.level = None
			self.activityPrizes = None
			self.marketPurpose = None
			self.recordId = None

		def getapiname(self):
			return 'jingdong.promo.unit.addIsvActivity'

			





