
from odoo import fields, models


class AttendanceReportWizard(models.TransientModel):
    _name = 'attendance.report.wizard'
    _description = 'Attendance Report Wizard'

    date = fields.Date(string='Month', required=True)
    employee_id = fields.Many2one(
        'hr.employee', string='Employee', readonly=True)

    def generate_report(self):

        data = {
            'form_data': self.read()[0],
        }
        return self.env.ref('hr_attendance_mitxelena.action_report_attendance').report_action(self, data=data)
