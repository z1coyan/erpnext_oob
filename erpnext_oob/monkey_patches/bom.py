from erpnext.manufacturing.doctype.bom.bom import BOM

def validate_uom_is_interger(self):
    pass

BOM.validate_uom_is_interger = validate_uom_is_interger