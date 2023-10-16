from seven_jd.jd.api.base import RestApi

class ImgzoneCategoryAddRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.cate_name = None
			self.parent_cate_id = None

		def getapiname(self):
			return 'jingdong.imgzone.category.add'

			





