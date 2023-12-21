import frappe
from pypinyin import lazy_pinyin


@frappe.whitelist()
def get_pinyin(source):
    p = lazy_pinyin(source, errors='ignore')
    #全拼 和 首字母拼
    return f"{''.join(p)} {''.join(a[0] for a in p)}"

def get_posting_date_month(doc, month_key):
    """posting_date = 2023-09-18 
       d_posting_date = > 18
       m_posting_date = > 09
       y_posting_date = > 23
       Y_posting_date = > 2023
    """

    if month_key in ('m_posting_date', 'm_posting_date', 'y_posting_date', 'Y_posting_date') and doc.posting_date:
        return frappe.utils.getdate(doc.posting_date).strftime(f"%{month_key[0]}")