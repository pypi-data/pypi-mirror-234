from seven_jd.jd.api.base import RestApi

class VcItemOldProductUpdateV2Request(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.apply_id = None
			self.leafCid = None
			self.pkg_info = None
			self.intro_mobile = None
			self.video_id = None
			self.original_place = None
			self.purchaser_code = None
			self.design_concept = None
			self.warranty = None
			self.tel = None
			self.cid1 = None
			self.danger_value = None
			self.store_property = None
			self.brand_id = None
			self.en_brand = None
			self.after_sale_desc = None
			self.web_site = None
			self.item_num = None
			self.sku_unit = None
			self.ware_id = None
			self.zh_brand = None
			self.saler_code = None
			self.has_transfer_elec_code = None
			self.name = None
			self.intro_html = None
			self.spuId = None
			self.upcSpuId = None
			self.prop_values = None
			self.prop_alias = None
			self.prop_vid = None
			self.prop_id = None
			self.prop_remark = None
			self.ocrUrl = None
			self.wreadme = None
			self.ext_id = None
			self.ext_values = None
			self.ext_alias = None
			self.ext_remark = None
			self.market_price_gaea = None
			self.dim1_val_gaea = None
			self.dim2_sort_gaea = None
			self.purchase_price_gaea = None
			self.sku_name_gaea = None
			self.item_num_gaea = None
			self.sku_short_title_gaea = None
			self.sku_id_gaea = None
			self.height_gaea = None
			self.member_price_gaea = None
			self.length_gaea = None
			self.weight_gaea = None
			self.upc_gaea = None
			self.dim1_sort_gaea = None
			self.dim2_val_gaea = None
			self.width_gaea = None
			self.structSaleAttrMap = None

		def getapiname(self):
			return 'jingdong.vc.item.oldProduct.updateV2'

			





