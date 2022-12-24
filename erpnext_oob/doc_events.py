import frappe
from pypinyin import lazy_pinyin


def pinyin_name(doc, method):
    if not doc.meta.has_field('pinyin_name'): return
    doc_before_save = doc.get_doc_before_save()
    if not doc_before_save or doc_before_save.customer_name != doc.customer_name:
        p =lazy_pinyin(doc.customer_name,errors='ignore')
        #全拼 和 首字母拼
        doc.pinyin_name = f"{''.join(p)} {''.join(a[0] for a in p)}"

def contact_image_handling(doc, method):
    if method == "before_validate" and not doc.image:
        doc.image = "dummy_image"
    elif method == "before_save" and doc.image == "dummy_image":
        doc.image = None