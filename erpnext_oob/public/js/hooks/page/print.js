frappe.ui.form.PrintView = class PrintPreview  extends frappe.ui.form.PrintView {
    show(frm) {
		this.frm = frm;
		this.set_title();
		this.set_breadcrumbs();
        //fisher 之前按单据类型默认打印格式，此处通过重新生成左边栏以实现按单据默认
        this.page && this.page.sidebar && this.page.sidebar.empty();
        this.setup_sidebar();

		this.setup_customize_dialog();

		// print format builder beta
        // fisher 加了这个变量
		this.inner_msg = this.page.add_inner_message(`
			<a style="line-height: 2.4" href="/app/print-format-builder-beta?doctype=${this.frm.doctype}">
				${__("Try the new Print Format Builder")}
			</a>
		`);
		
		let tasks = [
			this.set_default_print_format,
			this.set_default_print_language,
			this.set_default_letterhead,
			this.preview,
		].map((fn) => fn.bind(this));

		this.setup_additional_settings();
		return frappe.run_serially(tasks);
	}
    
    selected_format() {
        let current_print_format = this.print_format_selector.val();
        if (current_print_format){
            return current_print_format
        }
        //fisher 自动触发获取单据默认打印格式
        else {
            frappe.call({
                method: 'erpnext_oob.utils.get_print_format',
                args: {doc: this.frm.doc}
            }).then((r) =>{
                //console.log('r.message=', r.message);
                this.print_format_selector.val(r.message || this.frm.meta.default_print_format || 'Standard');
                this.refresh_print_format();
            })
        }
    }
}