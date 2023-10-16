from seven_jd.jd.api.base import RestApi

class JdAddressFromAddressGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.userid = None
			self.key = None
			self.provinceId = None
			self.cityId = None
			self.countryId = None
			self.townId = None
			self.address = None
			self.shipping = None

		def getapiname(self):
			return 'jingdong.JdAddressFromAddress.get'

			





