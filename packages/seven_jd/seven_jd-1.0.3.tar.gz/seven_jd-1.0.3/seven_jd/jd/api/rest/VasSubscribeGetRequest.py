from seven_jd.jd.api.base import RestApi

class VasSubscribeGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.user_name = None
			self.item_code = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.vas.subscribe.get'

			





