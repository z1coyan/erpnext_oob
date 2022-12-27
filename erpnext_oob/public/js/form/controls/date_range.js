// 时间区间语言没有设置

frappe.ui.form.ControlDateRange = class ControlDateRange extends frappe.ui.form.ControlDateRange {
    set_date_options() {
		super.set_date_options();
		let lang = "en";
		frappe.boot.user && (lang = frappe.boot.user.language);
		if($.fn.datepicker.language[lang]) {
			this.datepicker_options.language = lang
        }
	}
}

// frappe.ui.form.ControlDateRange = MyControlDateRange