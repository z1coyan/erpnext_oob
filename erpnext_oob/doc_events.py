import frappe
from erpnext_oob.api import get_pinyin
from erpnext_oob.localize.localize import import_coa


def pinyin_name(doc, method):
    if not doc.meta.has_field('pinyin_name'): return    
    doc.pinyin_name = get_pinyin(doc.customer_name)

def contact_image_handling(doc, method):
    if method == "before_validate" and not doc.image:
        doc.image = "dummy_image"
    elif method == "before_save" and doc.image == "dummy_image":
        doc.image = None

def company_create_default_accounts(doc, method):
    coa_exist = frappe.db.sql(
			"""select name from tabAccount
				where company=%s and docstatus<2 limit 1""",
			doc.name
		)
    if not coa_exist and doc.chart_of_accounts == '中国会计科目表' and not doc.is_new():
        doc.create_default_warehouses()
        frappe.local.flags.ignore_root_company_validation = True
        frappe.local.flags.ignore_chart_of_accounts = True      #bypass system to set default accounts
        import_coa(doc.name)        

    