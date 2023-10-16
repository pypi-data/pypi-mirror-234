from seven_jd.jd.api.base import RestApi

class EdiSdvWarePerformancedataGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.queryStartTime = None
			self.queryEndTime = None
			self.pageNum = None
			self.pageSize = None

		def getapiname(self):
			return 'jingdong.edi.sdv.ware.performancedata.get'

			





