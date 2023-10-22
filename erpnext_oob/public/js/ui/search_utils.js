//fisher 导入被调用函数
import { fuzzy_match } from "frappe/public/js/frappe/ui/toolbar/fuzzy_match.js";  

//fisher 支持中文或英文检索
frappe.search.utils.fuzzy_search = function (keywords = "", _item = "", return_marked_string = false) {
    let item = __(_item || '');
	let [, score, matches] = fuzzy_match(keywords, item, return_marked_string);
	// fisher 支持英文检索
	if (score == 0 && frappe.boot.lang != 'en' && item !== _item){
		item = _item || '';
		[, score, matches] = fuzzy_match(keywords, item, return_marked_string);
	}

	if (!return_marked_string) {
		return score;
	}
	if (score == 0) {
		return { score, item };
	}

	// Create Boolean mask to mark matching indices in the item string
	const matchArray = Array(item.length).fill(0);
	matches.forEach((index) => (matchArray[index] = 1));

	let marked_string = "";
	let buffer = "";

	// Clear the buffer and return marked matches.
	const flushBuffer = () => {
		if (!buffer) return "";
		const temp = `<mark>${buffer}</mark>`;
		buffer = "";
		return temp;
	};

	matchArray.forEach((isMatch, index) => {
		if (isMatch) {
			buffer += item[index];
		} else {
			marked_string += flushBuffer();
			marked_string += item[index];
		}
	});
	marked_string += flushBuffer();

	return { score, marked_string };
}