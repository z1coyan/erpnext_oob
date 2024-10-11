frappe.ui.form.ControlTable = class ControlTable extends frappe.ui.form.ControlTable {
	make() {
		super.make();
		this.$wrapper.off('paste', ':text');
		this.$wrapper.on('paste', ':text', e => {
			const table_field = this.df.fieldname;
			const table_field_event_handler = this.frm.events[table_field];
			const grid = this.grid;
			const grid_pagination = grid.grid_pagination;
			const grid_rows = grid.grid_rows;
			const doctype = grid.doctype;
			const row_docname = $(e.target).closest('.grid-row').data('name');
			const in_grid_form = $(e.target).closest('.form-in-grid').length;
			let pasted_data = frappe.utils.get_clipboard_data(e);

			if (!pasted_data || in_grid_form) return;

			let data = frappe.utils.csv_to_array(pasted_data, '\t');

			if (data.length === 1 && data[0].length === 1) return;

			let fieldnames = [];
			let child_rows = []
			// for raw data with column header
			if (this.get_field(data[0][0])) {
				data[0].forEach(column => {
					fieldnames.push(this.get_field(column));
				});
				data.shift();
			} else {
				// no column header, map to the existing visible columns
				const visible_columns = grid_rows[0].get_visible_columns();
				let target_column_matched = false;
				visible_columns.forEach(column => {
					// consider all columns after the target column.
					if (target_column_matched || column.fieldname === $(e.target).data('fieldname')) {
						fieldnames.push(column.fieldname);
						target_column_matched = true;
					}
				});
			}

			let row_idx = locals[doctype][row_docname].idx;
			let data_length = data.length;
			let tasks = [];	//setTimeout是异步函数，须确保明细行处理完了再处理整个明细表
			tasks.push(() => {
				data.forEach((row, i) => {
					let child_row = {};
					setTimeout(() => {
						let blank_row = !row.filter(Boolean).length;
						if (!blank_row) {
							if (row_idx > this.frm.doc[table_field].length) {
								this.grid.add_new_row();
							}
	
							if (row_idx > 1 && (row_idx - 1) % grid_pagination.page_length === 0) {
								grid_pagination.go_to_page(grid_pagination.page_index + 1);
							}
	
							const row_name = grid_rows[row_idx - 1].doc.name;						
							row.forEach((value, data_index) => {
								const fieldname =fieldnames[data_index];
								if (fieldname) {
									//fisher 保存文本编辑器字段的回车换行
									if (value) {
										const fieldtype = frappe.meta.get_field(doctype,fieldname).fieldtype;
										if (fieldtype){
											if (fieldtype ==='Text Editor') {
												value = value.replace(/[\n\r]/g,'<br>');
											} else if (['Float', 'Currency'].includes(fieldtype)) {
												value = parseFloat(value);
											} else if (fieldtype ==='Int') {
												value = parseInt(value);
											}
										}									
									 };
									if (!table_field_event_handler){ 
										frappe.model.set_value(doctype, row_name, fieldname, value);
									}else{	//如果有子表事件，则不触发明细行字段事件，由子表事件调用后台统一处理									
										child_row[fieldname] = value;
									}
								}
							});
							child_rows.push(child_row);
							console.log(child_row);
							row_idx++;
						}
						//fisher 移到外面来，复制的最后空行不会导致进度条走不完
						if (data_length >= 10) {
							let progress = i + 1;
							frappe.show_progress(__('Processing'), progress, data_length, null, true);
						}	
					}, 0);				
				});
			})
			
			tasks.push(() => {
				if (table_field_event_handler){
					table_field_event_handler(this.frm, child_rows);
				}			
			})

			frappe.run_serially(tasks);
			return false; // Prevent the default handler from running.
		});
	}
};