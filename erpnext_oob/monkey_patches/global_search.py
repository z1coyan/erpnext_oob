import frappe
from frappe.utils import global_search, cint


#_search = global_search.search

@frappe.whitelist()
def custom_search(text, start=0, limit=20, doctype=""):
	"""
	Search for given text in __global_search
	:param text: phrase to be searched
	:param start: start results at, default 0
	:param limit: number of results to return, default 20
	:return: Array of result objects
	"""
	from frappe.desk.doctype.global_search_settings.global_search_settings import (
		get_doctypes_for_global_search,
	)
	from frappe.query_builder.functions import Match

	results = []
	sorted_results = []

	allowed_doctypes = get_doctypes_for_global_search()

	for (idx, word) in enumerate(set(text.split("&"))):
		word = word.strip()
		if not word:
			continue

		global_search = frappe.qb.Table("__global_search")
		rank = Match(global_search.content).Against(word).as_("rank")
		query = (
			frappe.qb.from_(global_search)
			.select(global_search.doctype, global_search.name, global_search.content, rank)
			.orderby("rank", order=frappe.qb.desc)
            # fisher 20230806 添加过滤条件
			.where(rank > 0)
			.limit(limit)
		)

		if doctype:
			query = query.where(global_search.doctype == doctype)
		elif allowed_doctypes:
			query = query.where(global_search.doctype.isin(allowed_doctypes))

		if cint(start) > 0:
			query = query.offset(start)

		result = query.run(as_dict=True)

		if not idx:
			results.extend(result)            
		else:# 处理合并逻辑
			matched_docnames = {(r.doctype, r.name) for r in result}
			results = [r for r in results if (r.doctype, r.name) in matched_docnames]

	# sort results based on allowed_doctype's priority
	for doctype in allowed_doctypes:
		for index, r in enumerate(results):
			if r.doctype == doctype and r.rank > 0.0:
				try:
					meta = frappe.get_meta(r.doctype)
					if meta.image_field:
						r.image = frappe.db.get_value(r.doctype, r.name, meta.image_field)
				except Exception:
					frappe.clear_messages()

				sorted_results.extend([r])

	return sorted_results

#fisher 检查用户有权限才返回
@frappe.whitelist()
def search(text, start=0, limit=20, doctype=""):
    ret = []
    limit = int(limit)
    start = int(start)
    require_run_search = True
    result = []
    for i in range(100):
        if not require_run_search: break
        if i == 1:
            start += limit +1
        elif i > 1:
            start += limit
        
        result = custom_search(text, start, limit, doctype)
        if not result: break
        
        require_run_search = False
        for r in result:
            try:
                doc = frappe.get_doc(r.doctype, r.name)
                if doc.has_permission():
                    ret.append(r)
                    if len(ret) >= limit: break
                else:
                    require_run_search = True
            except frappe.DoesNotExistError:    #due to data inconsistency
                print('not exist',r.doctype, r.name, start)
                frappe.clear_messages()         #hide doc does not exist popup message seen by user
                require_run_search = True 
            
    return ret

global_search.search = search
