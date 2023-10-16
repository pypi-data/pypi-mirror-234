from seven_jd.jd.api.base import RestApi

class PopFwOrderListwithpageRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.pageSize = None
			self.fwsPin = None
			self.currentPage = None
			self.serviceCode = None

		def getapiname(self):
			return 'jingdong.pop.fw.order.listwithpage'

			





