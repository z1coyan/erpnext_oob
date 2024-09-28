
frappe.provide("frappe.form.formatters");

// 修改日期时间格式化， YYYY-MM-DD  HH:mm:ss
frappe.form.formatters.Datetime = function(value) {
	if(value) {
		var m = moment(frappe.datetime.convert_to_user_tz(value));
		if(frappe.boot.sysdefaults.time_zone) {
			m = m.tz(frappe.boot.sysdefaults.time_zone);
		}
		return m.format(frappe.boot.sysdefaults.date_format.toUpperCase() + ' HH:mm:ss');
	} else {
		return "";
	}
}

// data类型都会调用翻译方法,翻译报表中单据类型等字段
frappe.form.formatters.Data = function(value, df) {
	if (df && df.options == "URL") {
		if (!value) return;
		return `<a href="${value}" title="Open Link" target="_blank">${value}</a>`;
	}
	//表单中的子表单仅限启用了可翻译的数据字段才调用翻译函数
	if (frappe.get_route_str().includes('query-report') || df && df.translatable) {
		value = value == null ? "" : __(value);
	}

	return frappe.form.formatters._apply_custom_formatter(value, df);	
}

frappe.form.formatters.MultiSelect = function(value) {
	if (typeof value == "string") {
		return __(value);
	} else if (Array.isArray(value)) {
		return value.map(v => __(v));
	}
}