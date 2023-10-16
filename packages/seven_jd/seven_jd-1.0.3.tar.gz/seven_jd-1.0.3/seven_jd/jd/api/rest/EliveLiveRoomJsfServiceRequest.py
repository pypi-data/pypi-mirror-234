from seven_jd.jd.api.base import RestApi

class EliveLiveRoomJsfServiceRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.liveId = None
			self.appId = None

		def getapiname(self):
			return 'jingdong.elive.LiveRoomJsfService'

			





