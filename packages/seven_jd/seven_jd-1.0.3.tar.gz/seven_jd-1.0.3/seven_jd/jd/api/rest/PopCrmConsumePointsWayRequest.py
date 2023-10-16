from seven_jd.jd.api.base import RestApi

class PopCrmConsumePointsWayRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)

		def getapiname(self):
			return 'jingdong.pop.crm.consumePointsWay'

			





