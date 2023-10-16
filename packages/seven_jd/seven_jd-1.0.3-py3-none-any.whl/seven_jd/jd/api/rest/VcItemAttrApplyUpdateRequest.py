from seven_jd.jd.api.base import RestApi

class VcItemAttrApplyUpdateRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.apply_id = None
			self.public_name = None
			self.ware_ids = None
			self.dim1_vals = None
			self.dim1_sorts = None
			self.dim2_vals = None
			self.dim2_sorts = None
			self.dim1_attr = None
			self.dim2_attr = None
			self.other_dim_attr = None

		def getapiname(self):
			return 'jingdong.vc.item.attr.apply.update'

			





