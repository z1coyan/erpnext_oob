import json
import frappe
from frappe.integrations.doctype.webhook import webhook

def custom_get_webhook_data(doc, webhook):
	data = {}
	doc = doc.as_dict(convert_dates_to_str=True)

	if webhook.webhook_data:
		data = {w.key: doc.get(w.fieldname) for w in webhook.webhook_data}
	elif webhook.webhook_json:
		data = frappe.render_template(webhook.webhook_json, get_context(doc))
		# 加了strict=False
		data = json.loads(data, strict=False)

	return data

webhook.get_webhook_data = custom_get_webhook_data