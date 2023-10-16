from seven_jd.jd.api.base import RestApi

class FollowProductReadQueryForCountByProductIdRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.productId = None

		def getapiname(self):
			return 'jingdong.follow.product.read.queryForCountByProductId'

			





