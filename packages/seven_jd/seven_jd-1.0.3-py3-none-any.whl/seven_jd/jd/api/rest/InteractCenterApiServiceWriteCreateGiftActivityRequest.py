from seven_jd.jd.api.base import RestApi

class InteractCenterApiServiceWriteCreateGiftActivityRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appName = None
			self.isPrize = None
			self.batchKey = None
			self.prizeStartTime = None
			self.collectTimes = None
			self.prizeType = None
			self.desc = None
			self.discount = None
			self.couponId = None
			self.skuIds = None
			self.sendCount = None
			self.prizeId = None
			self.activityId = None
			self.prizeLevel = None
			self.quota = None
			self.prizeEndTime = None
			self.validateDay = None
			self.putKey = None
			self.modifier = None
			self.sourceLink = None
			self.isSinglePrize = None
			self.source = None
			self.type = None
			self.modelIds = None
			self.modified = None
			self.rfId = None
			self.startTime = None
			self.id = None
			self.validate = None
			self.isEverydayAward = None
			self.subtitleName = None
			self.created = None
			self.taskIds = None
			self.name = None
			self.sourceCloseLink = None
			self.pictureLink = None
			self.endTime = None
			self.sourceName = None
			self.supplierCode = None
			self.ext = None

		def getapiname(self):
			return 'jingdong.interact.center.api.service.write.createGiftActivity'

			





