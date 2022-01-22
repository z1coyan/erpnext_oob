class MyPermissionEngine  extends frappe.PermissionEngine{
    setup_page() {
		var me = this;
		this.doctype_select
			= this.wrapper.page.add_auto_select(__("Document Type"), this.options.doctypes, 
				function(e) {
					if (e.target.value) {
						frappe.set_route("permission-manager", e.target.value);
					}
				});
		this.role_select
			= this.wrapper.page.add_auto_select(__("Roles"), this.options.roles,
				function() {
					me.refresh();
				});

		this.page.add_inner_button(__('Set User Permissions'), () => {
			return frappe.set_route('List', 'User Permission');
		});
		this.set_from_route();
	}
	// fisher 取设在data-value属性上的实际值而不是显示标签值val()
	get_doctype() {
		let doctype = this.doctype_select.attr("data-value");
		return this.doctype_select.get(0).selectedIndex == 0 ? null : doctype;
	}

	get_role() {
		let role = this.role_select.attr("data-value");
		return this.role_select.get(0).selectedIndex == 0 ? null : role;
	}

	show_add_rule() {
		this.page.set_primary_action(
			__("Add A New Rule"),
			() => {
				let d = new frappe.ui.Dialog({
					title: __("Add New Permission Rule"),
					fields: [
						{
							fieldtype: "Autocomplete", label: __("Document Type"),
							options: this.options.doctypes, reqd: 1, fieldname: "parent"
						},
						{
							fieldtype: "Autocomplete", label: __("Role"),
							options: this.options.roles, reqd: 1, fieldname: "role"
						},
						{
							fieldtype: "Select", label: __("Permission Level"),
							options: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], reqd: 1, fieldname: "permlevel",
							description: __("Level 0 is for document level permissions, higher levels for field level permissions.")
						}
					]
				});
				if (this.get_doctype()) {
					d.set_value("parent", this.get_doctype());
					d.get_input("parent").prop("disabled", true);
				}
				if (this.get_role()) {
					d.set_value("role", this.get_role());
					d.get_input("role").prop("disabled", true);
				}
				d.set_value("permlevel", "0");
				d.set_primary_action(__('Add'), () => {
					let args = d.get_values();
					if (!args) {
						return;
					}
					frappe.call({
						module: "frappe.core",
						page: "permission_manager",
						method: "add",
						args: args,
						callback: (r) => {
							if (r.exc) {
								frappe.msgprint(__("Did not add"));
							} else {
								this.refresh();
							}
						}
					});
					d.hide();
				});
				d.show();
			},
			"small-add"
		);
	}
}

frappe.PermissionEngine = MyPermissionEngine;