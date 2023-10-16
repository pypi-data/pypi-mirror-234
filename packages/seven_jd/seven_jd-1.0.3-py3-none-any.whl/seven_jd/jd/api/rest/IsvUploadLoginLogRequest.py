from seven_jd.jd.api.base import RestApi

class IsvUploadLoginLogRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.result = None
			self.user_ip = None
			self.app_name = None
			self.josAppKey = None
			self.jd_id = None
			self.device_id = None
			self.user_id = None
			self.message = None
			self.time_stamp = None

		def getapiname(self):
			return 'jingdong.isv.uploadLoginLog'

			





