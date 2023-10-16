from seven_jd.jd.api.base import RestApi

class PopCustomerJosGetVenderCustomerByBindTimeRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.scrollId = None
			self.minBindingTime = None
			self.pageSize = None
			self.maxBindingTime = None

		def getapiname(self):
			return 'jingdong.pop.customer.jos.getVenderCustomerByBindTime'

			





