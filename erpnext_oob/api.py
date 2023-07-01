import frappe
from pypinyin import lazy_pinyin


@frappe.whitelist()
def get_pinyin(source):
    p = lazy_pinyin(source, errors='ignore')
    #全拼 和 首字母拼
    return f"{''.join(p)} {''.join(a[0] for a in p)}"