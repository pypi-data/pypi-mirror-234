from seven_jd.jd.api.base import RestApi

class RiskQueryServiceRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.param1 = None

		def getapiname(self):
			return 'jingdong.risk.QueryService'

			
	

class Param1(object):
		def __init__(self):
			"""
			"""
			self.appName = None
			self.time = None
			self.extendMap = None
			self.useType = None
			self.pin = None
			self.subSys = None
			self.open_id_buyer = None
			self.xid_buyer = None





