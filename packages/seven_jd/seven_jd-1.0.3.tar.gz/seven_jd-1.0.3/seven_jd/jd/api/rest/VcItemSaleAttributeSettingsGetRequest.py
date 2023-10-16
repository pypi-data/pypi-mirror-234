from seven_jd.jd.api.base import RestApi

class VcItemSaleAttributeSettingsGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.cid3 = None

		def getapiname(self):
			return 'jingdong.vc.item.saleAttributeSettings.get'

			





