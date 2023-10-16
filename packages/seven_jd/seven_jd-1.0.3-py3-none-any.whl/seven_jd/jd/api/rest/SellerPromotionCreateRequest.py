from seven_jd.jd.api.base import RestApi

class SellerPromotionCreateRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ip = None
			self.port = None
			self.request_id = None
			self.name = None
			self.beginTime = None
			self.endTime = None
			self.bound = None
			self.member = None
			self.slogan = None
			self.comment = None
			self.platform = None
			self.favorMode = None
			self.shopMember = None
			self.qqMember = None
			self.plusMember = None
			self.samMember = None
			self.tokenId = None
			self.promoChannel = None
			self.memberLevelOnly = None
			self.tokenUseNum = None
			self.allowOthersOperate = None
			self.allowOthersCheck = None
			self.allowOtherUserOperate = None
			self.allowOtherUserCheck = None
			self.needManualCheck = None
			self.previewsId = None
			self.previewsContent = None
			self.previewsTime = None
			self.skuIconId = None
			self.skuIconShowTime = None
			self.promoAreaType = None
			self.promoArea = None
			self.showTokenPrice = None
			self.skuId = None
			self.bindType = None
			self.promoPrice = None
			self.num = None
			self.wareId = None
			self.skuName = None
			self.jdPrice = None
			self.itemNum = None
			self.type = None
			self.propsNum = None
			self.usedWay = None
			self.couponValidDays = None
			self.freqBound = None
			self.perMaxNum = None
			self.perMinNum = None
			self.pin = None
			self.useBeginTime = None
			self.useEndTime = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.seller.promotion.create'

			





