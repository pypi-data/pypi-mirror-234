import datetime
from odoo import api, models, _
from odoo.exceptions import UserError, ValidationError

class ParticularReport(models.AbstractModel):
    _name = 'report.hr_attendance_mitxelena.report_hr_attendance_template'

    # def _get_report_values(self, docids, data=None):
    #     # get the report action back as we will need its data
    #     # report = self.env['ir.actions.report']._get_report_from_name('attendance_report.report_hr_attendance_template')
    #     # get the records selected for this rendering of the report
    #     # obj = self.env[report.model].browse(data['docids'])

    #     return {
    #         "docids": data['docids'],
    #         "doc_model": "hr.attendance",
    #     }

        # assistance_report = self.env['ir.actions.report']._get_report_from_name('hr_holidays.report_hr_attendance_template')
        # assistances = self.env['hr.assistance'].browse(self.ids)


    @api.model
    def _get_report_values(self, docids, data=None):
        
        if not data.get('form_data'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        if not data['form_data'].get('employee_id') and not data['form_data'].get('hr_employee_ids'):
            raise ValidationError(_("Invalid field selection; please select a particular data."))
        
        month_year = data['form_data'].get('date')
        month_year = month_year[0:7]
        # Extract the month name from the date
        data['month_name'] = datetime.datetime.strptime(month_year, '%Y-%m').strftime('%B')

        
        if data['form_data'].get('employee_id') or data['form_data'].get('hr_employee_ids'):
            employee = [data['form_data'].get('employee_id')[0]]
        docs = self.env['hr.employee'].browse(self.env.context.get('active_id'))

        assistances=[]
        if employee:
            for rec in employee:
                hr_employee_object = self.env['hr.employee'].browse(rec)
                dates_list = []
                vals_dict = {}
                # hr_attendance_obj = self.env['hr.attendance'].search([('employee_id', '=', hr_employee_object.id), ('check_in', '>=', start_date),('check_out', '<=', end_date)])
                hr_attendance_obj = self.env['hr.attendance'].search(
                 [('date', 'like', month_year + '%'), ('employee_id', '=', rec)])
                if not hr_attendance_obj:
                    raise UserError(_("No attendances found, this report cannot be printed."))

                by_days = {}
                resume_by_days = {}
                for times in hr_attendance_obj:
                    entry_date = times.date.strftime('%d-%m-%Y')
                    if entry_date in by_days.keys():
                        by_days[entry_date] = by_days[entry_date] + [times]
                    else:
                        by_days[entry_date] = [times]

                    vals_dict.update({'emp_name':hr_employee_object.name,
                                'vals': by_days,
                                })
                for day in by_days.keys():
                    expected_hours = hr_employee_object.resource_calendar_id.hours_per_day
                    day_worked_hours = 0
                    for entry in by_days[day]:
                        day_worked_hours += entry.worked_hours
                        factor = entry.entry_type.factor
                        if entry.entry_type.is_extra_time:
                            expected_hours = 0
                    day_extra_time = hr_attendance_obj.compute_day_extra_time(day_worked_hours, expected_hours)
                    day_extra_time_with_factor = hr_attendance_obj.compute_day_extra_time_with_factor(day_extra_time, factor)
                    resume_by_days[day] = [day_extra_time, day_extra_time_with_factor]

                ordered_dates = sorted(by_days.keys(), reverse=False)
                data['resume_by_days'] = resume_by_days
                data['hours_per_day'] = expected_hours

                # Crear un nuevo diccionario con las fechas en orden inverso
                by_days_ordered = {date: by_days[date] for date in ordered_dates}

                vals_dict.update({'emp_name': hr_employee_object.name,
                                'company_logo': hr_employee_object.company_id.logo,
                                'company_name': hr_employee_object.company_id.name,
                                'vals': by_days_ordered,
                                })

                assistances.append(vals_dict)

            return {
                'doc_ids': docids,
                'doc_model': 'hr.employee',
                'docs': assistances,
                'data': data,
            }
