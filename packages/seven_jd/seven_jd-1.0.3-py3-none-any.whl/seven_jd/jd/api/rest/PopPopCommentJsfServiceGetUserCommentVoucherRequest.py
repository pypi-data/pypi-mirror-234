from seven_jd.jd.api.base import RestApi

class PopPopCommentJsfServiceGetUserCommentVoucherRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ware2Type = None
			self.orderId = None
			self.beginRowNumber = None
			self.nickName = None
			self.ip = None
			self.nid = None
			self.isVenderReply = None
			self.ware3Type = None
			self.pageSize = None
			self.sort = None
			self.skuids = None
			self.wareName = None
			self.content = None
			self.score = None
			self.pin = None
			self.endRowNumber = None
			self.ware1Type = None
			self.guid = None
			self.beginTime = None
			self.endTime = None
			self.orderIds = None
			self.page = None
			self.replyPageSize = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.pop.PopCommentJsfService.getUserCommentVoucher'

			





