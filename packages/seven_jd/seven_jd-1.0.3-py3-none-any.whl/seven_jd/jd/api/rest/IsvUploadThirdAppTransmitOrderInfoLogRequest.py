from seven_jd.jd.api.base import RestApi

class IsvUploadThirdAppTransmitOrderInfoLogRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.app_name = None
			self.user_ip = None
			self.josAppKey = None
			self.device_id = None
			self.user_id = None
			self.order_ids = None
			self.sendto_url = None
			self.url = None
			self.time_stamp = None

		def getapiname(self):
			return 'jingdong.isv.uploadThirdAppTransmitOrderInfoLog'

			





