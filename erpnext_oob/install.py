# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import print_function, unicode_literals

import frappe


def after_install():
    frappe.db.set_value('System Settings','','enable_onboarding',0)
    frappe.db.commit()