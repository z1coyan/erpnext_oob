frappe.ui.form.on('Naming Series', {
	refresh(frm) {
		if (frappe.boot.user.language === 'zh'){
		    let help_html = frm.get_field('help_html');
		    let chinese_help = `<div class=\"well\">
    修改以下输入框中的单据编号模板. 规则:
    <ul>
        <li>每个编号模板一行.</li>
        <li>支持特殊字符 \"/\" 和 \"-\"</li>
        <li>
            可用点 (.)及其后的井号 (#)定义编号长度. 如, \".####\" 表示
            长度4位. 默认长度为5位.
        </li>
        <li>
            模板中可使用前后两个点(.)标识的变量
            <br>
            支持以下变量
            <ul>
                <li><code>.YYYY.</code> - 年 4位数字</li>
                <li><code>.YY.</code> - 年 2位数字</li>
                <li><code>.MM.</code> - 月</li>
                <li><code>.DD.</code> - 日</li>
                <li><code>.WW.</code> - 周</li>
                <li><code>.FY.</code> - 财年</li>
                <li>
                    <code>.{fieldname}.</code> - 单据字段，如
                    <code>branch</code>
                </li>
            </ul>
        </li>
    </ul>
    范例:
    <ul>
        <li>INV-</li>
        <li>INV-10-</li>
        <li>INVK-</li>
        <li>INV-.YYYY.-.{branch}.-.MM.-.####</li>
    </ul>
</div>`
		    help_html.html(chinese_help);
		}
	}
})