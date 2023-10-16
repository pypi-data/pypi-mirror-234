from seven_jd.jd.api.base import RestApi

class TemplateReadFindTemplatesByVenderIdRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.pageNo = None
			self.field = None

		def getapiname(self):
			return 'jingdong.template.read.findTemplatesByVenderId'

			





