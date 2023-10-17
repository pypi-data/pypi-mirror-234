from odoo import fields, models


class HrEntryType(models.Model):
    _name = "hr.entry.type"
    _description = "Entry Type"

    """
    Entry Type model.
    This will be used to define the corrective factor for each entry
    type's extra hours.
    """

    name = fields.Char(string="Name", required=True)
    factor = fields.Float(string="Corrective Factor", required=True, default=1.0)
    is_extra_time = fields.Boolean(
        string="Is extra time?", help="Is is true, all the time is consider extra hours"
    )
