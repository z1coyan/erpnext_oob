// 新加一个自动完成的选择框
frappe.ui.Page = class MyPage  extends frappe.ui.Page{
    add_auto_select(label, options, change) {
        let field = this.add_field({label:label, fieldtype:"Autocomplete", options: options, change: change});
		return field.$wrapper.find("input").empty();
	}
}