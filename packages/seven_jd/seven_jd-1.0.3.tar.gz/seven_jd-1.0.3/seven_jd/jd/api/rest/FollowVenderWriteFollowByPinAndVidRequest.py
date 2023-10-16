from seven_jd.jd.api.base import RestApi

class FollowVenderWriteFollowByPinAndVidRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.pin = None
			self.shopId = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.follow.vender.write.followByPinAndVid'

			





