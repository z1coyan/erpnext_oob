import frappe
import json
from frappe.exceptions import DoesNotExistError
from erpnext.stock.get_item_details import get_item_details
from erpnext.accounts.doctype.pricing_rule.pricing_rule import apply_pricing_rule
from six import string_types


@frappe.whitelist()
def get_user_default():
    return frappe.get_all("User Default", 
        filters = {'user': frappe.session.user},
        fields = ["setting_key", "setting_value"])

@frappe.whitelist()
def get_print_format(doc):
    if not frappe.db.has_column('Print Format', 'condition_for_default'):
        return

    if isinstance(doc, str):
        doc = json.loads(doc)
    doc = frappe.get_doc(doc)
    print_format_list =  frappe.get_all('Print Format', 
                                        filters = {'doc_type': doc.doctype,
                                                   'disabled': 0},
                                        fields = ['name', 'condition_for_default'],
                                        order_by = 'priority', as_list = 1)

    for (print_format, condition) in print_format_list:
        if condition and frappe.safe_eval(condition, None, dict(doc=doc, get_roles = frappe.get_roles)):
            return print_format

@frappe.whitelist()
def new_get_item_details(args, doc=None, for_validate=False, overwrite_warehouse=True):
    """fisher 修复旧物料切换到默认交易(采购、销售)单位与基本单位不同的新物料，单位转换率不自动刷新的问题"""
    if isinstance(args, string_types):
        args = json.loads(args)
    
    args.pop('conversion_factor', None)
    if args.get('doctype') == 'Sales Order':
        try:
            ret = get_item_details(args, doc=doc, for_validate=for_validate, overwrite_warehouse=overwrite_warehouse)
        except DoesNotExistError as e:
            customer_item_code = args.get('item_code')
            item_code = frappe.get_value('Item Customer Detail', 
                filters={'ref_code': customer_item_code}, fieldname='parent')   #'customer_name': args.get('customer')
            if item_code:
                args['item_code'] = item_code    
                ret = get_item_details(args, doc=doc, for_validate=for_validate, overwrite_warehouse=overwrite_warehouse)
                ret['customer_item_code'] = customer_item_code
                frappe.local.message_log.clear()
                frappe.local.response.pop('exc_type', None)
            else:
                raise
    else:
        ret = get_item_details(args, doc=doc, for_validate=for_validate, overwrite_warehouse=overwrite_warehouse)
    return ret

@frappe.whitelist()
def new_apply_pricing_rule(args, doc=None):
    if isinstance(args, string_types):
        args = json.loads(args)

    if args.get('doctype') == 'Sales Order':
        try:
            ret = apply_pricing_rule(args, doc=doc)
        except DoesNotExistError as e:
            customer_item_code = args.get('items')[0].get('item_code')
            item_code = frappe.get_value('Item Customer Detail', 
                filters={'ref_code': customer_item_code}, fieldname='parent')   #'customer_name': args.get('customer')
            if item_code:
                args.get('items')[0]['item_code'] = item_code    
                ret = apply_pricing_rule(args, doc=doc)
                frappe.local.message_log.clear()
                frappe.local.response.pop('exc_type', None)
            else:
                raise
    else:
        ret = apply_pricing_rule(args, doc=doc)
    return ret



"""{"items":[{"doctype":"Sales+Order+Item","name":"new-sales-order-item-4","child_docname":"new-sales-order-item-4","item_code":"test2","item_group":"成品(CP)","qty":2,"stock_qty":0,"stock_uom":"个","parenttype":"Sales+Order","parent":"new-sales-order-1","conversion_factor":1,"margin_type":""}],"customer":"东门子","customer_group":"所有客户组","territory":"所有区域","currency":"CNY","conversion_rate":1,"price_list":"标准销售","price_list_currency":"CNY","plc_conversion_rate":1,"company":"frappedemo","transaction_date":"2022-02-12","ignore_pricing_rule":0,"doctype":"Sales+Order","name":"new-sales-order-1","is_return":0,"update_stock":0,"pos_profile":""}"""