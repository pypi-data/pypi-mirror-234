from seven_jd.jd.api.base import RestApi

class PopPresellMyPresellServiceAddQualification4AppRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appName = None
			self.ip = None
			self.bu_Id = None
			self.systemKey = None
			self.ua = None
			self.pin = None
			self.sku = None

		def getapiname(self):
			return 'jingdong.pop.presell.MyPresellService.addQualification4App'

			





