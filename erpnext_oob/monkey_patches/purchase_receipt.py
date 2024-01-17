import frappe
from frappe.utils import flt
from pypika import functions as fn
from erpnext.stock.doctype.purchase_receipt import purchase_receipt
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import (
    adjust_incoming_rate_for_pr as original_adjust_incoming_rate_for_pr)

def custom_adjust_incoming_rate_for_pr(doc):
    """标准的采购入库与发票价差未剔除含税价中的税，修正这个问题
        取采购发票的未税金额net_amount取代之前的发票金额amount
    """

    billed_amt_map = get_billed_amount_against_pr([row.name for row in doc.items])
    for item in doc.items:
        billed_amt = billed_amt_map.get(item.name)
        if billed_amt and item.net_amount:            
            adjusted_amt = flt(billed_amt) - flt(item.net_amount)
            item.db_set("rate_difference_with_purchase_invoice", adjusted_amt, update_modified=False)

    original_adjust_incoming_rate_for_pr(doc)

purchase_receipt.adjust_incoming_rate_for_pr = custom_adjust_incoming_rate_for_pr

def get_billed_amount_against_pr(pr_items):
	purchase_invoice_item = frappe.qb.DocType("Purchase Invoice Item")

	query = (
		frappe.qb.from_(purchase_invoice_item)
        #fisher: 从之前的发票金额amount修改为取未税金额net_amount
		.select(fn.Sum(purchase_invoice_item.net_amount).as_("billed_amt"), purchase_invoice_item.pr_detail)
		.where((purchase_invoice_item.pr_detail.isin(pr_items)) & (purchase_invoice_item.docstatus == 1))
		.groupby(purchase_invoice_item.pr_detail)
	).run(as_dict=1)

	return {d.pr_detail: flt(d.billed_amt) for d in query}