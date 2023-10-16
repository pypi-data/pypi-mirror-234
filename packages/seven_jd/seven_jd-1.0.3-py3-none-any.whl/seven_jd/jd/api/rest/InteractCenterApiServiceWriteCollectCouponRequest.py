from seven_jd.jd.api.base import RestApi

class InteractCenterApiServiceWriteCollectCouponRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appName = None
			self.channel = None
			self.pin = None
			self.activityId = None
			self.ip = None
			self.ruleId = None
			self.rfId = None
			self.source = None
			self.type = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.interact.center.api.service.write.collectCoupon'

			





