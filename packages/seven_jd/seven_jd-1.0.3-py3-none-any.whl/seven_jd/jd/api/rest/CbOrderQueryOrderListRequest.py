from seven_jd.jd.api.base import RestApi


class CbOrderQueryOrderListRequest(RestApi):
    def __init__(self, domain='gw.api.360buy.com', port=80):
        """
		"""
        RestApi.__init__(self, domain, port)
        self.orderId = None
        self.syncBaseData = None
        self.deliveryType = None
        self.orderStatus = None
        self.queryCount = None
        self.bookTimeEnd = None
        self.carrierCode = None
        self.thirdOrderId = None
        self.bookTimeDesc = None
        self.bookTimeBegin = None
        self.channelId = None
        self.traceId = None
        self.ip = None
        self.appId = None
        self.opName = None
        self.businessIdentity = None
        self.scenario = None
        self.shopId = None
        self.saasTenantCode = None
        self.clientDto_venderId = None
        self.currentPage = None
        self.pageSize = None

    def getapiname(self):
        return 'shangling.cb.order.queryOrderList'
