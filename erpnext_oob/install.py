# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import print_function, unicode_literals

import frappe


uom_list = [
    '个',
    '只',
    '支',
    '件',
    '台',
    '套',
    '卷',
    '片',
    '条',
    '打',
    '箱',
    '包',
    '千米',
    '米',
    '分米',
    '厘米',
    '毫米  ',
    '毫克',
    '克',
    '千克',
    '吨  ',
    '立方厘米',
    '立方分米',
    '立方米  ',
    '平方米',
    '平方厘米',
    '平方分米',
    '平方毫米  ',
    '升',
    '毫升  ',
    '年',
    '月',
    '周',
    '日',
    '小时',
    '分钟',
    '秒  ',
    '两',
    '斤',
    '公斤  ',
    '摄氏度',
    '华氏度'
]

def after_install():    
    try:
        existing_uom_list = frappe.get_all('UOM', pluck ='name')
        existing_uom_set = {uom for uom in existing_uom_list}
        #globals().update(locals())
        new_uom_list = [uom for uom in uom_list if uom not in existing_uom_set]
        for uom in new_uom_list:
            
            frappe.get_doc({
                'doctype': 'UOM',
                'uom_name': uom,
                'enabled': 1}).insert(ignore_permissions = 1)
        frappe.db.set_value('UOM',{'name': ('not in', uom_list)},'enabled', 0)
        frappe.db.set_value('System Settings','','enable_onboarding',0)
        frappe.db.commit()
    except:
        pass