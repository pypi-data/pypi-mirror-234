from seven_jd.jd.api.base import RestApi

class VssPromotionQueryunitpromopagelistRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.ware_id = None
			self.promo_id = None
			self.promo_name = None
			self.create_time_begin = None
			self.create_time_end = None
			self.begin_time = None
			self.end_time = None
			self.promo_state = None
			self.audit_state = None
			self.page_index = None
			self.page_size = None

		def getapiname(self):
			return 'jingdong.vss.promotion.queryunitpromopagelist'

			





