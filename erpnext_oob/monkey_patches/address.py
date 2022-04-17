import frappe
from frappe.contacts.doctype.address import address

original_address_query = address.address_query

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def custom_address_query(doctype, txt, searchfield, start, page_len, filters):
    result = original_address_query(doctype, txt, searchfield, start, page_len, filters)
    searchfields = frappe.get_meta("Address").get_search_fields()
    if 'name' in searchfields: searchfields.remove('name')
    fields = ['name'] + searchfields
    filters = {'name':('in', [r[0] for r in result])}
    result = frappe.db.get_list('Address', fields = fields, filters = filters, as_list = True)
    return result
    
address.address_query = custom_address_query