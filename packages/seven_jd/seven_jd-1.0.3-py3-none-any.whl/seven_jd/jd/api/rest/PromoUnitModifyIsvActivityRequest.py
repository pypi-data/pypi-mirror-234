from seven_jd.jd.api.base import RestApi

class PromoUnitModifyIsvActivityRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.id = None
			self.categoryId = None
			self.name = None
			self.beginTime = None
			self.endTime = None
			self.imageUrl = None
			self.note = None
			self.channelType = None
			self.ruleType = None
			self.shared = None
			self.source = None
			self.isvUrl = None
			self.pluginName = None
			self.status = None
			self.callBackUrl = None

		def getapiname(self):
			return 'jingdong.promo.unit.modifyIsvActivity'

			





