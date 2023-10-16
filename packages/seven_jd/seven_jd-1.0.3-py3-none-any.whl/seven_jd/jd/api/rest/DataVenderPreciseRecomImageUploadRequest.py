from seven_jd.jd.api.base import RestApi

class DataVenderPreciseRecomImageUploadRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.image_name = None
			self.bytes = None
			self.md5 = None

		def getapiname(self):
			return 'jingdong.data.vender.precise.recom.image.upload'

			





