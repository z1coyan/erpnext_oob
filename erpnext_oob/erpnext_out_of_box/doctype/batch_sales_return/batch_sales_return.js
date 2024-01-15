// Copyright (c) 2024, yuzelin and contributors
// For license information, please see license.txt

frappe.ui.form.on('Batch Sales Return', {
	setup(frm){
		frm.set_query("delivery_note", "items", function(doc, cdt, cdn) {
			return {
				filters: {
					'docstatus': 1,
					'status': ['not in', ['Return Issued']],
					'company': frm.doc.company					
				}
			}
		});		
	},
	onload(frm){
		frappe.realtime.on('batch_created_sales_return', async function(data) {
			await frm.reload_doc();
			frm.trigger('show_return_delivery_list');	
		});
	},
	show_return_delivery_list(frm){
		const return_dns = frm.doc.items.map(r=>{return r.return_dn});
		if (return_dns && return_dns.length) {
			frappe.route_options = {
				"name": ['in', return_dns]
			}
			frappe.set_route('List', 'Delivery Note');						
		}
	},
	refresh: function(frm) {
		if (frm.doc.docstatus === 1){
			frm.add_custom_button(__('View Return Delivery Note'), () => {
				frm.trigger('show_return_delivery_list');
			});
		}
	}
});
