from seven_jd.jd.api.base import RestApi

class CrmMemberSearchNewRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.customer_pin = None
			self.grade = None
			self.min_last_trade_time = None
			self.max_last_trade_time = None
			self.min_trade_count = None
			self.max_trade_count = None
			self.avg_price = None
			self.min_trade_amount = None
			self.current_page = None
			self.page_size = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.crm.member.searchNew'

			





