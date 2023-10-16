from seven_jd.jd.api.base import RestApi

class CrmGradeUpdateRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.amount = None
			self.count = None

		def getapiname(self):
			return 'jingdong.crm.grade.update'

			





