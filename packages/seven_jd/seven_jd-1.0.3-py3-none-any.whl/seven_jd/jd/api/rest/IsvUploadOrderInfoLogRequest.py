from seven_jd.jd.api.base import RestApi

class IsvUploadOrderInfoLogRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.user_ip = None
			self.app_name = None
			self.josAppKey = None
			self.jd_id = None
			self.device_id = None
			self.user_id = None
			self.file_md5 = None
			self.order_ids = None
			self.operation = None
			self.url = None
			self.time_stamp = None

		def getapiname(self):
			return 'jingdong.isv.uploadOrderInfoLog'

			





