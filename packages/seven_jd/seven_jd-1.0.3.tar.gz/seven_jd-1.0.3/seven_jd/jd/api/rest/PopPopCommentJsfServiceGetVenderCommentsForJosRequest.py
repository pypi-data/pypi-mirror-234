from seven_jd.jd.api.base import RestApi

class PopPopCommentJsfServiceGetVenderCommentsForJosRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.skuids = None
			self.wareName = None
			self.beginTime = None
			self.endTime = None
			self.score = None
			self.content = None
			self.pin = None
			self.isVenderReply = None
			self.cid = None
			self.orderIds = None
			self.page = None
			self.pageSize = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.pop.PopCommentJsfService.getVenderCommentsForJos'

			





