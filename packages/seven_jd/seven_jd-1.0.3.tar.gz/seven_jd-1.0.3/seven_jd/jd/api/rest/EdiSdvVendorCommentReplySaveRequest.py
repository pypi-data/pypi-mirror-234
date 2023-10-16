from seven_jd.jd.api.base import RestApi

class EdiSdvVendorCommentReplySaveRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.username = None
			self.commentId = None
			self.type = None
			self.parentReplyId = None
			self.targetReplyId = None
			self.content = None
			self.venderId = None
			self.ip = None
			self.clientType = None
			self.uuid = None

		def getapiname(self):
			return 'jingdong.edi.sdv.vendor.comment.reply.save'

			





