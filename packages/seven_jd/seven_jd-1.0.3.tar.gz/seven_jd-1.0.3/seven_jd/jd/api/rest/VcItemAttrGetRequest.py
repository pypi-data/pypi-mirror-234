from seven_jd.jd.api.base import RestApi

class VcItemAttrGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.group_id = None

		def getapiname(self):
			return 'jingdong.vc.item.attr.get'

			





