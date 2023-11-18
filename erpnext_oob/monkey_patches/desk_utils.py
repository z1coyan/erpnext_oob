import frappe
from frappe.desk import utils


def provide_binary_file(filename: str, extension: str, content: bytes) -> None:
	"""Provide a binary file to the client.,
        fisher  solve the chinese filename not supported by gunicorn: latin encoding error
    """
	from frappe import _
	from urllib.parse import quote, unquote

	filename = f"{_(filename)}.{extension}"
	filename = f'{quote(unquote(filename))}'

	frappe.response["type"] = "binary"
	frappe.response["filecontent"] = content
	frappe.response["filename"] = filename

utils.provide_binary_file = provide_binary_file    