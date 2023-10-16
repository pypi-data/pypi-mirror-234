from seven_jd.jd.api.base import RestApi

class OpenApplyAppointmentRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.cityName = None
			self.sourceType = None
			self.ip = None
			self.appKey = None
			self.tenantCode = None
			self.provinceName = None
			self.productName = None

		def getapiname(self):
			return 'jingdong.open.applyAppointment'

			





