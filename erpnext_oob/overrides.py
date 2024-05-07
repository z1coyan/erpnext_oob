import frappe
from frappe.core.doctype.communication.communication import Communication
from frappe.core.doctype.file.utils import extract_images_from_html
from frappe.core.doctype.data_import.data_import import DataImport

class CustomCommunication(Communication):
    def get_content(self, print_format=None):
        #添加了系统设置值检查
        view_link = frappe.utils.cint(
            frappe.db.get_value("System Settings", "System Settings", "attach_view_link")
        )
        if print_format and view_link:
            return self.content + self.get_attach_link(print_format)
        return self.content

@frappe.whitelist()
def update_comment(name, content):
	"""allow only owner to update comment"""
	doc = frappe.get_doc("Comment", name)

	if frappe.session.user not in ["Administrator", doc.owner]:
		frappe.throw(_("Comment can only be edited by the owner"), frappe.PermissionError)
	if 	doc.reference_doctype and doc.reference_name:
		reference_doc = frappe.get_doc(doc.reference_doctype, doc.reference_name)	
		doc.content = extract_images_from_html(reference_doc, content, is_private=True)
	else:
		doc.content = content
	doc.save(ignore_permissions=True)

class CustomDataImport(DataImport):
	def validate_doctype(self):
		"""允许属性设置批量导入"""
		
		if self.reference_doctype != "Property Setter":
			super().validate_doctype()