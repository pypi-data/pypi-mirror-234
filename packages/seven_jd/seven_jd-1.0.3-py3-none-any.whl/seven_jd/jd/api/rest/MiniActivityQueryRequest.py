from seven_jd.jd.api.base import RestApi

class MiniActivityQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.size = None
			self.page = None
			self.status = None
			self.scene = None

		def getapiname(self):
			return 'jingdong.mini.activity.query'

			





