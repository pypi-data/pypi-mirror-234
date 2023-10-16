from seven_jd.jd.api.base import RestApi

class CategoryReadFindValuesByAttrIdUnlimitRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.categoryAttrId = None
			self.field = None

		def getapiname(self):
			return 'jingdong.category.read.findValuesByAttrIdUnlimit'

			





