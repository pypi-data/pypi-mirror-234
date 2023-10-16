from seven_jd.jd.api.base import RestApi

class InteractCenterApiServiceWriteWritePersonInfoRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appName = None
			self.channel = None
			self.pin = None
			self.profileUrl = None
			self.activityId = None
			self.created = None
			self.startTime = None
			self.id = None
			self.endTime = None
			self.type = None
			self.actionType = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.interact.center.api.service.write.writePersonInfo'

			





