from seven_jd.jd.api.base import RestApi

class PrintingPrintDataSensitivePullDataRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.param1 = None

		def getapiname(self):
			return 'jingdong.printing.printData.sensitivePullData'

			
	

class Attribute1(object):
		def __init__(self):
			"""
			"""
			self.orderNo = None
			self.ewPrintData = None
			self.wayBillNo = None


class Param1(object):
		def __init__(self):
			"""
			"""
			self.objectId = None
			self.parameters = None
			self.cpCode = None
			self.ewPrintDataInfos = None





