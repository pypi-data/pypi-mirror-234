from seven_jd.jd.api.base import RestApi


class DirectlyZeusTaskBusinessCheckRequest(RestApi):
    def __init__(self, domain='gw.api.360buy.com', port=80):
        """
			"""
        RestApi.__init__(self, domain, port)
        self.source = None
        self.businessId = None

    def getapiname(self):
        return 'jingdong.directly.zeus.task.business.check'
