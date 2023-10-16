from seven_jd.jd.api.base import RestApi

class PopCrmShopGiftCreateShopGiftRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.name = None
			self.startDate = None
			self.endDate = None
			self.modelIds = None
			self.creator = None
			self.createChannel = None
			self.closeLink = None
			self.isvName = None
			self.activityLink = None
			self.requestPin = None
			self.isvValidate = None
			self.sendNumber = None
			self.open_id_seller = None
			self.xid_seller = None
			self.open_id_isv = None
			self.xid_isv = None
			self.discount = None
			self.quota = None
			self.validateDay = None
			self.prizeType = None
			self.sendCount = None

		def getapiname(self):
			return 'jingdong.pop.crm.shopGift.createShopGift'

			





