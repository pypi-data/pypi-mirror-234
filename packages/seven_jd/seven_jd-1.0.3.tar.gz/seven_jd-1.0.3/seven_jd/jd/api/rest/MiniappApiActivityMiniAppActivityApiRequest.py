from seven_jd.jd.api.base import RestApi

class MiniappApiActivityMiniAppActivityApiRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.activityMsg = None
			self.name = None
			self.startTime = None
			self.endTime = None
			self.activityUuid = None
			self.scene = None

		def getapiname(self):
			return 'jingdong.miniapp.api.activity.MiniAppActivityApi'

			





