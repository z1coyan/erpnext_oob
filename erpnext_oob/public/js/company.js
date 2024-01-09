frappe.ui.form.on("Company", {
    refresh(frm){
        frm.set_query("disposal_account", function() {			
			return {
				filters: {
					company: frm.docname,
                    disabled: 0,					
					is_group: 0
				}
			}
		});
    }
})