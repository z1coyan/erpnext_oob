import frappe
import json
from frappe import _
from frappe.core.doctype.data_import.importer import Importer


def export_errored_rows(self):
    from frappe.utils.csvutils import build_csv_response
    from urllib.parse import quote, unquote

    if not self.data_import:
        return

    import_log = (
        frappe.get_all(
            "Data Import Log",
            fields=["row_indexes", "success"],
            filters={"data_import": self.data_import.name},
            order_by="log_index",
        )
        or []
    )

    failures = [log for log in import_log if not log.get("success")]
    row_indexes = []
    for f in failures:
        row_indexes.extend(json.loads(f.get("row_indexes", [])))

    # de duplicate
    row_indexes = list(set(row_indexes))
    row_indexes.sort()

    header_row = [col.header_title for col in self.import_file.columns]
    rows = [header_row]
    rows += [row.data for row in self.import_file.data if row.row_number in row_indexes]
    #fisher 加了quote解决 gunicorn 不能解析中文文件名问题
    build_csv_response(rows, quote(_(self.doctype)))

Importer.export_errored_rows = export_errored_rows