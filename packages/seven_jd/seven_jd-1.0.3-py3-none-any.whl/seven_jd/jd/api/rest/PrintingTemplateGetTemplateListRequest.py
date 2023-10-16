from seven_jd.jd.api.base import RestApi

class PrintingTemplateGetTemplateListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.param1 = None

		def getapiname(self):
			return 'jingdong.printing.template.getTemplateList'

			
	

class Param1(object):
		def __init__(self):
			"""
			"""
			self.templateId = None
			self.templateType = None
			self.wayTempleteType = None
			self.cpCode = None
			self.isvResourceType = None





