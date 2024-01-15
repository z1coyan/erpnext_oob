# Copyright (c) 2024, yuzelin and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return

class BatchSalesReturn(Document):
	def validate(self):
		self.validate_dn()

	def validate_dn(self):
		dn_list = frappe.get_all('Delivery Note',
			filters = {'name': ('in', {row.delivery_note for row in self.items}),
						'docstatus': 1,
						'company': self.company,
						'status': ('not in', ('Return Issued'))},
			fields = ['name','`tabDelivery Note Item`.item_code','`tabDelivery Note Item`.qty']
		)
		dn_map = {(row.name,row.item_code):row.qty for row in dn_list}
		for row in self.items:
			dn_qty = dn_map.get((row.delivery_note, row.item_code))
			row.error = ''
			if not dn_qty:
				row.error = _('dn and item code not valid, either dn is not submitted or already returned')
			elif row.return_qty > dn_qty:
				row.error = _('Return Qty greater than delivery qty')

	def on_submit(self):
		if [row for row in self.items if row.error]:
			frappe.throw(_('Please remove the rows with error'))
		self.make_return_delivery()
	
	def make_return_delivery(self):
		"""
		{ dn1: {item1:qty,item2:qty}
		  dn1: {item1:qty,item2:qty}
		}"""
		dn_map = {}
		dn_return_dn_map = {}
		for row in self.items:
			dn_map.setdefault(row.delivery_note, {})[row.item_code] = row.return_qty
		
		for (dn, items_dict) in dn_map.items():
			return_dn = make_sales_return(dn)
			return_dn.items = [row for row in return_dn.items if row.item_code in items_dict]
			for row in return_dn.items:
				row.qty = items_dict.get(row.item_code)
				row.stock_qty = row.qty * row.conversion_factor
			return_dn = return_dn.insert(ignore_permissions = 1)
			dn_return_dn_map[dn] = return_dn.name
		for (dn, return_dn) in dn_return_dn_map.items():
			frappe.db.set_value(self.items[0].doctype,
				{
					'parent': self.name,
				 	'delivery_note': dn
				},
				'return_dn',
				return_dn)		
		frappe.publish_realtime("batch_created_sales_return", doctype=self.doctype, docname=self.name)