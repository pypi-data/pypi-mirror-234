from seven_jd.jd.api.base import RestApi

class VssReportJosSearchBrandPerformanceInfoRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.searchType = None
			self.year = None
			self.month = None
			self.daysCode = None
			self.pageIndex = None
			self.pageSize = None

		def getapiname(self):
			return 'jingdong.vss.report.jos.searchBrandPerformanceInfo'

			





