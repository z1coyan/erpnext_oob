
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import importlib

import frappe

patches_loaded = False

__version__ = '15.0.26'


def console(*data):
    frappe.publish_realtime("out_to_console", data, user=frappe.session.user)


def load_monkey_patches():
    global patches_loaded

    if (
        patches_loaded
        or not getattr(frappe, "conf", None)
        or not "erpnext_oob" in frappe.get_installed_apps()
    ):
        return

    for app in frappe.get_installed_apps():
        if app in ['frappe', 'erpnext']: continue
        try:
            folder = frappe.get_app_path(app, "monkey_patches")
            if os.path.exists(folder):
                for module_name in os.listdir(folder):
                    if not module_name.endswith(".py") or module_name == "__init__.py":
                        continue
                    importlib.import_module(f"{app}.monkey_patches.{module_name[:-3]}")
        except:
            frappe.log(f'{app} load failed in erpnext_oob, check whether you removed the app')        

    patches_loaded = True


connect = frappe.connect


def custom_connect(*args, **kwargs):
    out = connect(*args, **kwargs)

    if frappe.conf.auto_commit_on_many_writes:
        frappe.db.auto_commit_on_many_writes = 1

    load_monkey_patches()
    return out


frappe.connect = custom_connect