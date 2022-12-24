frappe.PermissionEngine = class PermissionEngine  extends frappe.PermissionEngine {
    setup_page() {
		var me = this;
		me.doctype_select
			= me.wrapper.page.add_auto_select(__("Document Type"), me.options.doctypes, 
				function(e) {
					console.log(e);
					if (e && e.target && e.target.value) {
						frappe.set_route("permission-manager", e.target.value);
					}
				});
		me.role_select
			= me.wrapper.page.add_auto_select(__("Roles"), me.options.roles,
				function() {
					me.refresh();
				});

		me.page.add_inner_button(__('Set User Permissions'), () => {
			return frappe.set_route('List', 'User Permission');
		});
		me.set_from_route();
	}
	// fisher 取设在data-value属性上的实际值而不是显示标签值val()
	get_doctype() {
		var me = this;
		let doctype = me.doctype_select.attr("data-value");
		return !me.doctype_select.val()? null : doctype;
	}

	get_role() {
		var me = this;
		let role = me.role_select.attr("data-value");
		return !me.role_select.val()? null : role;
	}

	add_check(cell, d, fieldname, label, description = "") {
		label = fieldname === "select"? "Select Link": label;
		return super.add_check(cell, d, fieldname, label, description)
	}
}