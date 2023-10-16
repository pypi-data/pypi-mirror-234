from seven_jd.jd.api.base import RestApi

class PopBeanSendBeanRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.requestId = None
			self.beanNum = None
			self.accountId = None
			self.accountCode = None
			self.sendWay = None
			self.sendCode = None
			self.accountType = None
			self.context = None
			self.planId = None
			self.rfId = None
			self.open_id_buyer = None
			self.xid_buyer = None

		def getapiname(self):
			return 'jingdong.pop.bean.sendBean'

			





