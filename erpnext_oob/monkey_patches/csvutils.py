import frappe
from frappe.utils.csvutils import to_csv
from frappe.utils import csvutils, cstr


def build_csv_response(data, filename):
    from urllib.parse import quote, unquote

    filename = f'{quote(unquote(filename))}'     #fisher 处理中文文件名
    data = cstr(to_csv(data))
    data = f'{quote(unquote(data))}'
    frappe.response["result"] = data
    frappe.response["doctype"] = filename
    frappe.response["type"] = "csv"


#csvutils.build_csv_response = build_csv_response  #fisher 不能在这里修复，因为进入这个方法就以经报错了！