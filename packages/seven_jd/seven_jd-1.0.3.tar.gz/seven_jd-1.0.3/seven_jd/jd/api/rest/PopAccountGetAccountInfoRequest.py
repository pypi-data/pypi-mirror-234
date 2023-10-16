from seven_jd.jd.api.base import RestApi

class PopAccountGetAccountInfoRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.accountType = None
			self.accountCode = None

		def getapiname(self):
			return 'jingdong.pop.account.getAccountInfo'

			





