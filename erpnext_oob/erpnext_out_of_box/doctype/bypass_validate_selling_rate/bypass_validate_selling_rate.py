# Copyright (c) 2022, yuzelin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BypassValidateSellingRate(Document):
	def validate(self):
		if self.type != 'Item Group':
			self.item_group = ''
		elif self.type != 'Item Code':
			self.item_code = '' 

	def on_update(self):
		clear_bypass_validate_selling_rate_cache(self.company)

	def on_trash(self):
		clear_bypass_validate_selling_rate_cache(self.company)

def clear_bypass_validate_selling_rate_cache(company):
	frappe.cache().hdel('bypass_validate_selling_rate', company)