from seven_jd.jd.api.base import RestApi


class DirectlyZeusTaskCompleteRequest(RestApi):
    def __init__(self, domain='gw.api.360buy.com', port=80):
        """
			"""
        RestApi.__init__(self, domain, port)
        self.source = None
        self.openId = None
        self.encrypt = None

    def getapiname(self):
        return 'jingdong.directly.zeus.task.complete'
