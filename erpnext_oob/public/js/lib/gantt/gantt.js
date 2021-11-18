let MyGanttView = class MyGanttView extends frappe.views.GanttView {
    get required_libs() {
		return [
			"assets/erpnext_oob/js/lib/gantt/frappe-gantt.css",
			"assets/erpnext_oob/js/lib/gantt/frappe-gantt.min.js"
		];
	}
}

frappe.views.GanttView = MyGanttView