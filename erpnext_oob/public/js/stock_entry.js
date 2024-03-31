frappe.listview_settings['Stock Entry'] = {
    formatters: {
		"stock_entry_type": function(value, df, doc) {
			return __(value);
		}
	}
}  