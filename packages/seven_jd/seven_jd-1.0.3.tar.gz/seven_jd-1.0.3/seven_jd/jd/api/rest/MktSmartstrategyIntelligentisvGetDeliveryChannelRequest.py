from seven_jd.jd.api.base import RestApi

class MktSmartstrategyIntelligentisvGetDeliveryChannelRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.value = None

		def getapiname(self):
			return 'jingdong.mkt.smartstrategy.intelligentisv.getDeliveryChannel'

			





