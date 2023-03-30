from frappe.core.doctype.communication.communication import Communication

class CustomCommunication(Communication):
    def get_content(self, print_format=None):
        #添加了系统设置值检查
        view_link = frappe.utils.cint(
            frappe.db.get_value("System Settings", "System Settings", "attach_view_link")
        )
        if print_format and view_link:
            return self.content + self.get_attach_link(print_format)
        return self.content