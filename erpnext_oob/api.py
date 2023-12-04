import frappe
from pypinyin import lazy_pinyin


@frappe.whitelist()
def get_pinyin(source):
    p = lazy_pinyin(source, errors='ignore')
    #全拼 和 首字母拼
    return f"{''.join(p)} {''.join(a[0] for a in p)}"

def get_posting_date_month(doc, month_key):
    if month_key == 'MM_posting_date' and doc.posting_date:
        return frappe.utils.getdate(doc.posting_date).strftime("%m")