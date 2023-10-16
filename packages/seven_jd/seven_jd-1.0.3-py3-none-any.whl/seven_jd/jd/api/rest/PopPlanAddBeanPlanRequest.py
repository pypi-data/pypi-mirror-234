from seven_jd.jd.api.base import RestApi

class PopPlanAddBeanPlanRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.requestId = None
			self.serviceMoneyBudget = None
			self.accountCode = None
			self.accountType = None
			self.sendTimes = None
			self.type = None
			self.modifyMode = None
			self.content = None
			self.accountId = None
			self.budgetNum = None
			self.name = None
			self.rfId = None
			self.beginTime = None
			self.endTime = None
			self.sendMode = None
			self.sendRule = None
			self.pinRiskLevel = None

		def getapiname(self):
			return 'jingdong.pop.plan.addBeanPlan'

			





