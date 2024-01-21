# Copyright (c) 2024, yuzelin and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, today
from frappe.query_builder.functions import Sum
from frappe.model.document import Document
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return

class BatchSalesReturn(Document):
	def validate(self):
		self.validate_dn()

	def validate_dn(self):
		dn = frappe.qb.DocType('Delivery Note')
		dni = frappe.qb.DocType('Delivery Note Item')

		dn_list = frappe.qb.from_(dn
		).join(dni
		).on(dn.name == dni.parent
		).where(				
			(dn.company == self.company) &
			(dn.docstatus == 1) &
			(dn.status.notin(('Return Issued','Cancelled','Closed'))) &
			((dni.qty - dni.returned_qty) > 0) &
			(dn.name.isin({row.delivery_note for row in self.items}))
		).select(
			dn.name,
			dni.item_code,
			Sum(dni.qty - dni.returned_qty).as_('qty')
		).groupby(dn.name,	dni.item_code
		).run(as_dict = 1)
		
		dn_map = {(row.name,row.item_code):row.qty for row in dn_list}
		for row in self.items:
			dn_qty = dn_map.get((row.delivery_note, row.item_code))
			row.error = ''
			row.return_qty = abs(flt(row.return_qty)) * -1
			if not dn_qty:
				row.error = _('dn and item code not valid, either dn is not submitted or already returned')
			elif abs(row.return_qty) > dn_qty:
				row.error = _('Return Qty {0} greater than returnable qty {1}').format(abs(row.return_qty), dn_qty)

	def on_submit(self):
		if [row for row in self.items if row.error]:
			frappe.throw(_('Please remove the rows with error'))
		self.set_default_return_date()
		self.make_return_delivery()

	def set_default_return_date(self):
		frappe.db.set_value(self.items[0].doctype,
		{
			'parent': self.name,
			'return_date': ('is', 'not set')
		},
		'return_date',
		today())

	def make_return_delivery(self):
		"""
		处理一个出库单中相同物料出现多次
		同一个出库单按多个退货日期退货（一次性补退货单）
		{ (dn1, return_date): {item1:qty,item2:qty}
		}"""
		dn_map = {}
		dn_return_dn_map = {}
		for row in self.items:
			dn_map.setdefault((row.delivery_note, row.return_date or today()), {})[row.item_code] = row.return_qty
		
		for ((dn,return_date), items_dict) in dn_map.items():
			return_dn = make_sales_return(dn)
			#globals().update(locals())
			if return_date != today():
				return_dn.set_posting_time = 1
				return_dn.posting_date = return_date
			items = []
			
			for row in return_dn.items:
				if row.item_code in items_dict and row.qty:
					pending_return_qty = items_dict.get(row.item_code)
					#退货数量是负数所以用>=					
					if row.qty < pending_return_qty:
						row.qty = pending_return_qty
						row.stock_qty = row.qty * row.conversion_factor						
					items.append(row)
					items_dict[row.item_code] -= row.qty
					if items_dict[row.item_code] >= 0:
						break
			return_dn.items = items
			return_dn.run_method("calculate_taxes_and_totals")	
			return_dn = return_dn.insert(ignore_permissions = 1)
			dn_return_dn_map[(dn, return_date)] = return_dn.name
			
		for ((dn, return_date), return_dn) in dn_return_dn_map.items():
			frappe.db.set_value(self.items[0].doctype,
				{
					'parent': self.name,
				 	'delivery_note': dn,
					'return_date': return_date
				},
				'return_dn',
				return_dn)		
		frappe.publish_realtime("batch_created_sales_return", doctype=self.doctype, docname=self.name)