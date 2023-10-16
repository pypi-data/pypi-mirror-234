from seven_jd.jd.api.base import RestApi

class PopOrderModifyVenderRemarkRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.order_id = None
			self.flag = None
			self.remark = None

		def getapiname(self):
			return 'jingdong.pop.order.modifyVenderRemark'

			





