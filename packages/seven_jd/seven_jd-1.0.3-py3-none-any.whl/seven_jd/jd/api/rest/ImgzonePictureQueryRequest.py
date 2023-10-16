from seven_jd.jd.api.base import RestApi

class ImgzonePictureQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.picture_id = None
			self.picture_cate_id = None
			self.picture_name = None
			self.start_date = None
			self.end_Date = None
			self.page_num = None
			self.page_size = None

		def getapiname(self):
			return 'jingdong.imgzone.picture.query'

			





