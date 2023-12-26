import frappe
from frappe.utils import cint
from frappe.permissions import rights
from frappe import permissions

def custom_get_role_permissions(doctype_meta, user=None, is_owner=None):
	"""
	Returns dict of evaluated role permissions like
	        {
	                "read": 1,
	                "write": 0,
	                // if "if_owner" is enabled
	                "if_owner":
	                        {
	                                "read": 1,
	                                "write": 0
	                        }
	        }
    fisher:修复权限角色管理勾选仅限创建者和导出时，用户仍然无法导出问题
	"""
	if isinstance(doctype_meta, str):
		doctype_meta = frappe.get_meta(doctype_meta)  # assuming doctype name was passed

	if not user:
		user = frappe.session.user

	cache_key = (doctype_meta.name, user, bool(is_owner))

	if user == "Administrator":
		return allow_everything()

	if not frappe.local.role_permissions.get(cache_key):
		perms = frappe._dict(if_owner={})

		roles = frappe.get_roles(user)

		def is_perm_applicable(perm):
			return perm.role in roles and cint(perm.permlevel) == 0

		def has_permission_without_if_owner_enabled(ptype):
			return any(p.get(ptype, 0) and not p.get("if_owner", 0) for p in applicable_permissions)

		applicable_permissions = list(
			filter(is_perm_applicable, getattr(doctype_meta, "permissions", []))
		)
		has_if_owner_enabled = any(p.get("if_owner", 0) for p in applicable_permissions)
		perms["has_if_owner_enabled"] = has_if_owner_enabled

		for ptype in rights:
			pvalue = any(p.get(ptype, 0) for p in applicable_permissions)
			# check if any perm object allows perm type
			perms[ptype] = cint(pvalue)
			if (
				pvalue
				and has_if_owner_enabled
				and not has_permission_without_if_owner_enabled(ptype)
				and ptype != "create"
			):
				perms["if_owner"][ptype] = cint(pvalue and is_owner)
				# has no access if not owner
				# only provide select or read access so that user is able to at-least access list
				# (and the documents will be filtered based on owner sin further checks)
				perms[ptype] = 1 if ptype in ("select", "read", "export") else 0   #fisher 增加了export

		frappe.local.role_permissions[cache_key] = perms

	return frappe.local.role_permissions[cache_key]

permissions.get_role_permissions = custom_get_role_permissions    