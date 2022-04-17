import frappe
from frappe.model import meta

#解决无法导入doctype的问题，加了labels
DOCTYPE_TABLE_FIELDS = [
	frappe._dict({"fieldname": "fields", "options": "DocField", "label":"Fields"}),
	frappe._dict({"fieldname": "permissions", "options": "DocPerm", "label":"Permissions"}),
	frappe._dict({"fieldname": "actions", "options": "DocType Action", "label":"Actions"}),
	frappe._dict({"fieldname": "links", "options": "DocType Link", "label":"Links"}),
]

meta.DOCTYPE_TABLE_FIELDS = DOCTYPE_TABLE_FIELDS