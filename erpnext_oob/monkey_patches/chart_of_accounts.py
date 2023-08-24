# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import json
import os

import frappe
from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import get_chart as original_get_chart


def get_chart(chart_template, existing_company=None):
    if not chart_template in ['中国小企业会计准则', '中国企业会计准则']:
        return original_get_chart(chart_template, existing_company)
    else:		
        path = frappe.get_app_path('erpnext_oob','localize/chart_of_account')
        fname = frappe.as_unicode(chart_template)    
        with open(os.path.join(path, f'{fname}.json'), "r") as f:
            chart = f.read()
            if chart and json.loads(chart).get("name") == chart_template:
                return json.loads(chart).get("tree")