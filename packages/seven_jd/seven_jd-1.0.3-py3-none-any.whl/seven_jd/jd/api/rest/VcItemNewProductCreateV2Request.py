from seven_jd.jd.api.base import RestApi

class VcItemNewProductCreateV2Request(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.apply_id = None
			self.leaf_cid = None
			self.pkg_info = None
			self.intro_mobile = None
			self.video_id = None
			self.purchase_price = None
			self.short_title = None
			self.original_place = None
			self.purchaser_code = None
			self.design_concept = None
			self.warranty = None
			self.model = None
			self.tel = None
			self.cid1 = None
			self.height = None
			self.product_oil_unit = None
			self.weight = None
			self.upc = None
			self.danger_value = None
			self.brand_id = None
			self.name = None
			self.en_brand = None
			self.market_price = None
			self.pack_type = None
			self.packing = None
			self.after_sale_desc = None
			self.web_site = None
			self.item_num = None
			self.gifts_goods = None
			self.pdfUrl = None
			self.intro_html = None
			self.shelf_life = None
			self.member_price = None
			self.length = None
			self.saler_code = None
			self.sysp = None
			self.width = None
			self.zh_brand = None
			self.spuId = None
			self.upcSpuId = None
			self.store_property = None
			self.has_transfer_elec_code = None
			self.product_oil_number = None
			self.sku_unit = None
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
			self.height_gaea = None
			self.member_price_gaea = None
			self.length_gaea = None
			self.weight_gaea = None
			self.upc_gaea = None
			self.dim1_sort_gaea = None
			self.dim2_val_gaea = None
			self.width_gaea = None
			self.end_date = None
			self.ent_code = None
			self.qc_code = None
			self.type = None
			self.applicant = None
			self.file_key_list = None
			self.structSaleAttrMap = None

		def getapiname(self):
			return 'jingdong.vc.item.newProduct.createV2'

			





