from seven_jd.jd.api.base import RestApi

class JosOauthRpcXidMixPin2XidRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appKey = None
			self.mixPin = None

		def getapiname(self):
			return 'jingdong.jos.oauth.rpc.xid.mixPin2Xid'

			





