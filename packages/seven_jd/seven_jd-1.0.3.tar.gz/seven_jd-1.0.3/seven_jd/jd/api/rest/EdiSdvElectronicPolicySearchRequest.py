from seven_jd.jd.api.base import RestApi

class EdiSdvElectronicPolicySearchRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.startTime = None
			self.endTime = None
			self.page = None
			self.pageSize = None

		def getapiname(self):
			return 'jingdong.edi.sdv.electronic.policy.search'

			





