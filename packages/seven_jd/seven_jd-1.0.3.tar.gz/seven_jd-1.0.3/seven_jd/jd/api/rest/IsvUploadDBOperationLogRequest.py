from seven_jd.jd.api.base import RestApi

class IsvUploadDBOperationLogRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.user_ip = None
			self.app_name = None
			self.josAppKey = None
			self.device_id = None
			self.user_id = None
			self.url = None
			self.db = None
			self.sql = None
			self.time_stamp = None

		def getapiname(self):
			return 'jingdong.isv.uploadDBOperationLog'

			





