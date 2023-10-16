from seven_jd.jd.api.base import RestApi

class TemplateWriteUpdateRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.bottomContent = None
			self.headContent = None
			self.id = None
			self.name = None
			self.mobileBottomContent = None
			self.mobileHeadContent = None

		def getapiname(self):
			return 'jingdong.template.write.update'

			





