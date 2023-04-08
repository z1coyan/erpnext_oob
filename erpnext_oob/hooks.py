from . import __version__ as app_version

app_name = "erpnext_oob"
app_title = "ERPNext Out Of Box"
app_publisher = "yuzelin"
app_description = "ERPNext Out of Box"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "yuxinyong@163.com"
app_license = "MIT"

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                (
                    "Item-min_pack_qty",
                ),
            ]
        ],
    },
    {
        "doctype": "Property Setter",
        "filters": [
            [
                "name",
                "in",
                (
                    'Stock Reconciliation-naming_series-options',
                    'Material Request-naming_series-options',
                    'Production Plan-naming_series-options',
                    'Quality Inspection-naming_series-options',
                    'Pick List-naming_series-options',
                    'Work Order-naming_series-options',
                    'Journal Entry-naming_series-options',
                    'Stock Entry-naming_series-options',
                    'Purchase Receipt-naming_series-options',
                    'Delivery Note-naming_series-options',
                    'Purchase Invoice-naming_series-options',
                    'Sales Invoice-naming_series-options',
                    'Purchase Order-naming_series-options',
                    'Sales Order-naming_series-options',
                    'Contact-last_name-hidden',
                    'User-full_name-hidden',
                    'User-last_name-hidden',
                    'User-middle_name-hidden',
                    'Contact-middle_name-hidden',
                    'Purchase Order-subscription_section-hidden',
                    'Customer-pan-hidden',
                    'Supplier-pan-hidden',
                    'Sales Order-set_warehouse-label',
                    'DocPerm-select-label',
                    'Bank Account-account_subtype-label',
                    'Bank Account-account_type-label',
                    'Bank Account-account_name-label',
                    'Purchase Receipt Item-manufacture_details-label',
                    'Material Request Item-manufacture_details-label',
                    'Supplier Quotation Item-manufacture_details-label',
                    'Purchase Order Item-manufacture_details-label',
                    'Purchase Invoice Item-manufacture_details-label',
                    'Task-weight-label',
                    'Advance Taxes and Charges-rate-label',
                    'Purchase Taxes and Charges-rate-label',
                    'Sales Taxes and Charges-rate-label'
                ),
            ]
        ],
    }
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_oob/css/erpnext_oob.css"
# app_include_js = "/assets/erpnext_oob/js/erpnext_oob.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_oob/css/erpnext_oob.css"
# web_include_js = "/assets/erpnext_oob/js/erpnext_oob.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "erpnext_oob/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

app_include_js = ["erpnext_oob.bundle.js"]
page_js = {
	"permission-manager": "public/js/hooks/page/permission_manager.js",
    "dashboard-view": "public/js/hooks/page/dashboard.js",
    "print": "public/js/hooks/page/print.js"
}
doctype_js = {
}

setup_wizard_requires = "assets/erpnext_oob/js/setup_wizard.js"

standard_queries = {
	"DocType": "erpnext_oob.localize.queries.doctype_role_report_query",
	"Role": "erpnext_oob.localize.queries.doctype_role_report_query",
	"Report": "erpnext_oob.localize.queries.doctype_role_report_query"
}
override_whitelisted_methods = {
    "frappe.desk.form.utils.update_comment": "erpnext_oob.overrides.update_comment",
 	"erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts.get_charts_for_country": "erpnext_oob.localize.localize.get_charts_for_country",
    #"erpnext.stock.get_item_details.get_item_details":"erpnext_oob.utils.new_get_item_details",
    "erpnext.accounts.doctype.pricing_rule.pricing_rule.apply_pricing_rule":"erpnext_oob.utils.new_apply_pricing_rule"
}
# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "erpnext_oob.install.before_install"
after_install = "erpnext_oob.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_oob.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Communication": "erpnext_oob.overrides.CustomCommunication"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
 	"Customer": {
 		"validate": "erpnext_oob.doc_events.pinyin_name"
	},
    "Contact": {
 		"before_validate": "erpnext_oob.doc_events.contact_image_handling",
        "before_save": "erpnext_oob.doc_events.contact_image_handling"
	},
    "Company": {
 		"after_insert": "erpnext_oob.doc_events.company_create_default_accounts",
        "validate": "erpnext_oob.doc_events.company_create_default_accounts"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_oob.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_oob.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_oob.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_oob.tasks.weekly"
# 	]
# 	"monthly": [
# 		"erpnext_oob.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "erpnext_oob.install.before_tests"


# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "erpnext_oob.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------



# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"erpnext_oob.auth.validate"
# ]

