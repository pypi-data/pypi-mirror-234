from seven_jd.jd.api.base import RestApi


class DirectlyZeusRewardProcessQueryRequest(RestApi):
    def __init__(self, domain='gw.api.360buy.com', port=80):
        """
		"""
        RestApi.__init__(self, domain, port)
        self.source = None
        self.pin = None
        self.open_id_buyer = None
        self.xid_buyer = None

    def getapiname(self):
        return 'jingdong.directly.zeus.reward.process.query'
