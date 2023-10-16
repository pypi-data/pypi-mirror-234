from seven_jd.jd.api.base import RestApi

class MiniappApiActivityMiniAppActivityApiUpdateActivityStatusRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.activityUuid = None
			self.status = None

		def getapiname(self):
			return 'jingdong.miniapp.api.activity.miniAppActivityApi.updateActivityStatus'

			





