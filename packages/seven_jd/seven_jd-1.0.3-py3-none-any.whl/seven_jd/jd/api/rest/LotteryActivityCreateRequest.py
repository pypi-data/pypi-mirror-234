from seven_jd.jd.api.base import RestApi

class LotteryActivityCreateRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.client = None
			self.awardsActivityInfo = None

		def getapiname(self):
			return 'jingdong.lottery.activity.create'

			
	

class Client(object):
		def __init__(self):
			"""
			"""
			self.appName = None
			self.appId = None
			self.channel = None
			self.requestIP = None
			self.timestamp = None


class AwardsRuleDTO(object):
		def __init__(self):
			"""
			"""
			self.awardsImgUrl = None
			self.awardsLevel = None
			self.awardsContent = None
			self.awardsQuatity = None
			self.lotteryMode = None
			self.lotteryNum = None
			self.awardsName = None


class AwardsDTO(object):
		def __init__(self):
			"""
			"""
			self.awardsRuleDTOList = None
			self.awardsType = None


class AwardsActivityInfo(object):
		def __init__(self):
			"""
			"""
			self.applyEndTime = None
			self.activityEndTime = None
			self.awardsDTOList = None
			self.test = None
			self.name = None
			self.activityStartTime = None
			self.type = None
			self.applyStartTime = None
			self.activityImgUrl = None
			self.worth = None





