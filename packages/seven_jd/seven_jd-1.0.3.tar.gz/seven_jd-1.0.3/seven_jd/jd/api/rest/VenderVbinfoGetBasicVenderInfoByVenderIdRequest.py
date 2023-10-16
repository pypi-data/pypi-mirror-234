from seven_jd.jd.api.base import RestApi

class VenderVbinfoGetBasicVenderInfoByVenderIdRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.colNames = None
			self.source = None

		def getapiname(self):
			return 'jingdong.vender.vbinfo.getBasicVenderInfoByVenderId'

			





