from seven_jd.jd.api.base import RestApi

class CreateMemberCardRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.memberCardInfoDTO = None

		def getapiname(self):
			return 'jingdong.createMemberCard'

			
	

class MemberCardInfoDTO(object):
		def __init__(self):
			"""
			"""
			self.birthday = None
			self.gender = None
			self.type = None
			self.pin = None
			self.phone = None
			self.organizations = None
			self.name = None
			self.openTime = None
			self.channelCode = None
			self.open_id_buyer = None
			self.xid_buyer = None





