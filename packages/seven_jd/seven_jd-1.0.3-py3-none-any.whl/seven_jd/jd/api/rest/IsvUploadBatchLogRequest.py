from seven_jd.jd.api.base import RestApi

class IsvUploadBatchLogRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.josAppKey = None
			self.data = None
			self.time_stamp = None
			self.type = None

		def getapiname(self):
			return 'jingdong.isv.uploadBatchLog'

			





