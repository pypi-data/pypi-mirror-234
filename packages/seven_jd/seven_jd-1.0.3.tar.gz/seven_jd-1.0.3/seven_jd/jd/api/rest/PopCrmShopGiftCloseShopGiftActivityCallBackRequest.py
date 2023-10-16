from seven_jd.jd.api.base import RestApi

class PopCrmShopGiftCloseShopGiftActivityCallBackRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.clientSource = None
			self.shopGiftContentDTO = None

		def getapiname(self):
			return 'jingdong.pop.crm.shopGift.closeShopGiftActivityCallBack'

			
	

class ClientSource(object):
		def __init__(self):
			"""
			"""
			self.appName = None
			self.channel = None


class ShopGiftContentDTO(object):
		def __init__(self):
			"""
			"""
			self.activityId = None





