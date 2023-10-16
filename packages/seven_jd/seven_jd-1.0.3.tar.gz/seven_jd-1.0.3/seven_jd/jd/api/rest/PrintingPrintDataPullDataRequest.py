from seven_jd.jd.api.base import RestApi

class PrintingPrintDataPullDataRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.param1 = None

		def getapiname(self):
			return 'jingdong.printing.printData.pullData'

			
	

class Attribute1(object):
		def __init__(self):
			"""
			"""
			self.orderNo = None
			self.popFlag = None
			self.wayBillCode = None
			self.jdWayBillCode = None


class Param1(object):
		def __init__(self):
			"""
			"""
			self.objectId = None
			self.parameters = None
			self.wayBillInfos = None
			self.cpCode = None





