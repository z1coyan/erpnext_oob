import re
from frappe.model.naming import parse_naming_series
from frappe.model import naming

"""
将自动编号格式化字符串 JE-{YY}{MM}{#####} 按分隔符.,-,{,}，去掉花括号，输出带分隔符的列表
string = "JE-{YY}{MM}{#####}"
['JE', '-', 'YY', 'MM', '#####']
"""
pattern = re.compile(r"(\{[^\{\}]+\})|(-)|(\.)|({)|(})") 

def custom_format_autoname(autoname, doc):
    """    
    解决未按年/月重新编号问题
    """

    first_colon_index = autoname.find(":")
    autoname_value = autoname[first_colon_index + 1 :]

    parts = pattern.split(autoname_value)
    parts = [part.replace("{","").replace("}", "") for part in parts if part]
    name = parse_naming_series(parts, doc=doc)
    
    return name

naming._format_autoname = custom_format_autoname