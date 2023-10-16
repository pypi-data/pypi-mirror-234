from seven_jd.jd.api.base import RestApi

class TemplateWriteBindWareRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.templateId = None
			self.wareId = None

		def getapiname(self):
			return 'jingdong.template.write.bindWare'

			





