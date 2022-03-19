import frappe


def execute():
	"""property setter to change field label does not work for this special core doctype"""
	
	sql = """update 
				tabDocField 
			set 
				label = 'Select Link'
			where
				fieldname='select' and parent like '%DocPerm'
   		"""
	frappe.db.sql(sql)

