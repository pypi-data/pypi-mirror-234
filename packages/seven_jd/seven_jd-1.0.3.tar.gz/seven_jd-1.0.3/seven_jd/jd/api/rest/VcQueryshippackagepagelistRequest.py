from seven_jd.jd.api.base import RestApi

class VcQueryshippackagepagelistRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.brand_id = None
			self.page_index = None
			self.page_size = None
			self.create_time_begin = None
			self.create_time_end = None

		def getapiname(self):
			return 'jingdong.vc.queryshippackagepagelist'

			





