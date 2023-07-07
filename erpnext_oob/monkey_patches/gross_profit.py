import frappe
from frappe import _, qb, scrub
from frappe.utils import cint, flt, formatdate
from erpnext.accounts.report.gross_profit.gross_profit import GrossProfitGenerator


def process(self):
    self.grouped = {}
    self.grouped_data = []

    self.currency_precision = cint(frappe.db.get_default("currency_precision")) or 3
    self.float_precision = cint(frappe.db.get_default("float_precision")) or 2

    grouped_by_invoice = True if self.filters.get("group_by") == "Invoice" else False

    if grouped_by_invoice:
        buying_amount = 0
    last_indent, buying_amount = 0.0, frappe._dict() #初始化, 各层级累计汇总{2.0:0,1.0:0} 	
    for row in reversed(self.si_list):
        if self.filters.get("group_by") == "Monthly":
            row.monthly = formatdate(row.posting_date, "MMM YYYY")

        if self.skip_row(row):
            continue

        row.base_amount = flt(row.base_net_amount, self.currency_precision)

        product_bundles = []
        if row.update_stock:
            product_bundles = self.product_bundles.get(row.parenttype, {}).get(row.parent, frappe._dict())
        elif row.dn_detail:
            product_bundles = self.product_bundles.get("Delivery Note", {}).get(
                row.delivery_note, frappe._dict()
            )
            row.item_row = row.dn_detail
            # Update warehouse and base_amount from 'Packed Item' List
            if product_bundles and not row.parent:
                # For Packed Items, row.parent_invoice will be the Bundle name
                product_bundle = product_bundles.get(row.parent_invoice)
                if product_bundle:
                    for packed_item in product_bundle:
                        if (
                            packed_item.get("item_code") == row.item_code
                            and packed_item.get("parent_detail_docname") == row.item_row
                        ):
                            row.warehouse = packed_item.warehouse
                            row.base_amount = packed_item.base_amount

        # get buying amount
        if row.item_code in product_bundles:
            row.buying_amount = flt(
                self.get_buying_amount_from_product_bundle(row, product_bundles[row.item_code]),
                self.currency_precision,
            )
        else:
            row.buying_amount = flt(self.get_buying_amount(row, row.item_code), self.currency_precision)

        if grouped_by_invoice:
            # if row.indent == 1.0:
            # 	buying_amount += row.buying_amount
            # elif row.indent == 0.0:
            # 	row.buying_amount = buying_amount
            # 	buying_amount = 0
            if row.indent != last_indent:
                if row.indent < last_indent: #切换到套件或发票	
                    row.buying_amount = buying_amount[last_indent]
                    buying_amount[last_indent] = 0
                if row.indent == 0.0:
                    buying_amount = frappe._dict()
            buying_amount[row.indent] = buying_amount.get(row.indent,0) + row.buying_amount
            last_indent = row.indent

        # get buying rate
        if flt(row.qty):
            row.buying_rate = flt(row.buying_amount / flt(row.qty), self.float_precision)
            row.base_rate = flt(row.base_amount / flt(row.qty), self.float_precision)
        else:
            if self.is_not_invoice_row(row):
                row.buying_rate, row.base_rate = 0.0, 0.0

        # calculate gross profit
        row.gross_profit = flt(row.base_amount - row.buying_amount, self.currency_precision)
        if row.base_amount:
            row.gross_profit_percent = flt(
                (row.gross_profit / row.base_amount) * 100.0, self.currency_precision
            )
        else:
            row.gross_profit_percent = 0.0

        # add to grouped
        self.grouped.setdefault(row.get(scrub(self.filters.group_by)), []).append(row)

    if self.grouped:
        self.get_average_rate_based_on_group_by()

GrossProfitGenerator.process = process