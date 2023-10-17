from calendar import monthrange
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from datetime import timedelta, datetime
from pytz import timezone
from logging import getLogger
_logger = getLogger(__name__)


class HrAttendanceMitxelena(models.Model):
    _inherit = 'hr.attendance'

    is_holiday = fields.Boolean(compute='_compute_is_holiday', store=True)

    is_relevo = fields.Boolean(compute='_compute_is_relevo', store=True)

    shift_type = fields.Selection([
        ('', _('Unknown')),
        ('morning', _('Morning')),
        ('afternoon', _('Afternoon')),
        ('night', _('Night')),
    ], compute='_compute_shift_type', store=True)

    consecutive_days = fields.Integer(
        compute='_compute_consecutive_days', store=True, default=1)

    entry_type = fields.Many2one('hr.entry.type', compute='_compute_entry_type', store=True)

    extra_time = fields.Float(
        compute='_compute_extra_time', store=True, default=0)

    extra_time_with_factor = fields.Float(
        compute='_compute_extra_time_with_factor', store=True, default=0)

    @api.depends('check_in', 'is_relevo', 'shift_type')
    def _compute_entry_type(self):
        for record in self:            
            if record.is_holiday:
                record.entry_type = self.env.ref('hr_attendance_mitxelena.holiday').id
                continue
            if record.consecutive_days > 5:
                record.entry_type = self.env.ref('hr_attendance_mitxelena.6th_day').id                
            elif record.count_as_weekend():
                record.entry_type = self.env.ref('hr_attendance_mitxelena.weekend').id
                if record.check_in.weekday() == 5 and record.shift_type == 'morning':
                    record.entry_type = self.env.ref('hr_attendance_mitxelena.saturday_morning').id
            elif record.is_relevo and record.shift_type != 'night':
                record.entry_type = self.env.ref('hr_attendance_mitxelena.relevo').id
            elif record.is_relevo and record.shift_type == 'night':   
                record.entry_type = self.env.ref('hr_attendance_mitxelena.relevo_night').id
            else:
                record.entry_type = 'not computed'
                _logger.error('Entry type not computed for %s', record)

    def count_as_weekend(self):
        # Get user timezone, or use Europe/Madrid as default
        tz = timezone(self.env.user.tz or 'Europe/Madrid')
        self.ensure_one()
        check_in = self.check_in.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
        # if is holiday, is not weekend
        if self.is_holiday:
            return False
        # if check_in is in Sunday but shift_type is night, is not weekend
        if check_in.weekday() == 6 and self.shift_type == 'night':
            return False
        # if check_in is between Monday and Friday, is not weekend
        if check_in.weekday() < 5:
            return False
        return True

    @api.depends('check_in', 'consecutive_days')
    def _compute_is_relevo(self):
        for record in self:           
            tz = timezone(record.env.user.tz or 'Europe/Madrid')
            check_in = record.check_in.replace(
                        tzinfo=timezone('UTC')).astimezone(tz)

            # if consecutive_days is bigger than 5, is not relevo
            if record.consecutive_days > 5:
                record.is_relevo = False
                continue
            
            # if is holiday, is not relevo
            if record.is_holiday:
                record.is_relevo = False
                continue

            # if check_in is between Monday and Friday, is relevo
            weekday = check_in.weekday()
            if weekday < 5:
                record.is_relevo = True
                continue

            #  if check_in is in Sunday but shift_type is night, is relevo        
            if check_in.weekday() == 6 and record.shift_type == 'night':
                record.is_relevo = True
                continue


    @api.depends('check_in')
    def _compute_is_holiday(self):
        holiday_model = self.env['hr.holidays.public']
        for record in self:
            if record.check_in:
                # Check if the check_in date is a public holiday
                record.is_holiday = holiday_model.is_public_holiday(
                    record.check_in.date())
            else:
                # If there is no check_in, we can't compute if it's a holiday
                record.is_holiday = False

    @api.depends('check_out')
    def _compute_shift_type(self):
        # Get user timezone, or use Europe/Madrid as default
        tz = timezone(self.env.user.tz or 'Europe/Madrid')
        for record in self:
            if record.check_in and record.check_out:
                # Convert check_in and check_out to local time
                check_in = record.check_in.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                check_out = record.check_out.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                midpoint = check_in + (check_out - check_in) / 2
                hour = midpoint.hour
                if 5 <= hour < 13:
                    shift_type = 'morning'
                elif 13 <= hour < 21:
                    shift_type = 'afternoon'
                else:
                    shift_type = 'night'
                record.shift_type = shift_type

    @api.depends('check_in', 'shift_type', 'worked_hours')
    def _compute_consecutive_days(self):
        for record in self:
            # If there is no check_in, set consecutive days to 0
            # and break the loop
            if not record.check_in:
                record.consecutive_days = 0
                return record.consecutive_days

            # Get the last 7 days range
            datetime_end = record.check_in
            datetime_start = datetime_end - timedelta(days=6)

            # Only select attendances where worked_hours > 0.5 hours
            # to avoid erroneous short attendances
            attendance_records = record.env['hr.attendance'].search([
                ('employee_id', '=', record.employee_id.id),
                ('check_in', '>=', datetime_start),
                ('check_in', '<=', datetime_end),
                ('worked_hours', '>', 0.5)
            ], order='check_in desc')

            # Init inner-loop variables
            previous_record = None
            consecutive_days = 1
            _logger.debug('[%s][%i][Init] Counting consecutive days',
                            record.id, consecutive_days)

            # If there are no attendance records, set consecutive days to 1
            # and break the loop
            if len(attendance_records) == 0:
                record.consecutive_days = 1
                _logger.debug('[%s][%i] No previous attendance records found',
                                record.id, consecutive_days)
                return consecutive_days

            # Iterate over the past attendance records
            for rec in attendance_records:
                _logger.debug(
                    '[%s] Checking past attendance %s', record.id, rec)

                # If there is no previous record, set it to the current one
                # and continue the loop
                if not previous_record:
                    previous_record = rec
                    _logger.debug(
                        '[%s] No previous record found, setting %s',
                        record.id, rec)
                    continue

                check_in_date = rec.check_in.date()
                previous_check_in_date = previous_record.check_in.date()

                # If the previous record it's not within the last day
                # break the loop and stop counting consecutive days
                is_consecutive = (previous_check_in_date -
                                    check_in_date) <= timedelta(days=1)

                if not is_consecutive:
                    _logger.debug(
                            '[%s] Records are not consecutive (%s)',
                            record.id, rec.id)
                    break

                # If the previous record it is not the same day,
                # add a consecutive day and continue the loop
                if previous_check_in_date != check_in_date:
                    consecutive_days += 1
                    _logger.debug('[%s] +1 consecutive days: %i',
                                    record.id, consecutive_days)
                    previous_record = rec
                    continue
                    
                # If the previous record has less than 2 hours worked,
                # skip this record and continue the loop                    
                if rec.worked_hours < 2:
                    _logger.debug(
                        '[%s] Same day, but less than 2 hours worked (%s)',
                        record.id, rec.id)                    
                    previous_record = rec
                    continue

                time_difference = previous_record.check_in - rec.check_out
                
                # If the previous record it's more than 7 hours
                # from the current one, add a consecutive day
                if (time_difference >= timedelta(hours=7)):                        
                    _logger.debug(
                        '[%s] Same day, but more than 7 hours difference',
                        record.id)
                    
                    consecutive_days += 1

                    _logger.debug(
                        '[%s] so, +1 consecutive days: %i', record.id, 
                        consecutive_days)
                                
                    # Set the previous record to the current one
                    previous_record = rec

            # Set the final consecutive days count to the record
            record.consecutive_days = consecutive_days

            _logger.debug('[%s][%i][Final] Consecutive days for %s has ended.',
                    record.id, consecutive_days, record.employee_id.name)
    
    def recompute_all(self, domain=None):
        # Get all records  from hr.attendance and iterate over them
        attendance_records = self.env['hr.attendance'].search(domain)
        _logger.debug('Attendance records: %s', attendance_records)
        for record in attendance_records:
            _logger.debug('Updating %s', record)
            record.is_holiday = record._compute_is_holiday()
            _logger.debug('Is holiday: %s', record.is_holiday)
            record.shift_type = record._compute_shift_type()
            _logger.debug('Shift type: %s', record.shift_type)
            record.consecutive_days = record._compute_consecutive_days()
            _logger.debug('Consecutive days: %s', record.consecutive_days)
            record.is_relevo = record._compute_is_relevo()
            _logger.debug('Is relevo: %s', record.is_relevo)
            record.entry_type = record._compute_entry_type()
            _logger.debug('Entry type: %s', record.entry_type)
            record.extra_time = record._compute_extra_time()
            _logger.debug('Extra time: %s', record.extra_time)
            _logger.debug('Extra time with factor: %s', record.extra_time_with_factor)


    def recompute_shifts(self):
        tz = timezone(self.env.user.tz or 'Europe/Madrid')
        attendance_records = self.env['hr.attendance'].search([])
        _logger.debug('Attendance records: %s', attendance_records)
        for record in attendance_records:
            try:
                check_in = record.check_in.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                check_out = record.check_out.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                midpoint = check_in + (check_out - check_in) / 2
                hour = midpoint.hour
                if 5 <= hour < 13:
                    shift_type = 'morning'
                elif 13 <= hour < 21:
                    shift_type = 'afternoon'
                else:
                    shift_type = 'night'
                record.shift_type = shift_type
                _logger.debug('Shift type %s for %s', shift_type, record)
                if record.shift_type != shift_type:
                    _logger.error('Shift type is %s for %s',
                                  record.shift_type, record)
                record._compute_consecutive_days()
            except Exception as e:
                _logger.error(
                    'Error computing shift type for %s: %s', record, e)

    def is_workshop_worker(self):
        for record in self:
            if record.employee_id.resource_calendar_id.name == 'Taller':
                return True
            else:
                return False

# TODO: Add calendars via data files and reference them here
    @api.depends('worked_hours')
    def _compute_extra_time(self):
        for record in self:
            theorical_hours = record.employee_id.resource_calendar_id.hours_per_day
            extra_time = self.compute_day_extra_time(
                record.worked_hours, theorical_hours)
            # If the entry type is an extra time entry and there was extra time,
            # set the extra time to the worked hours
            if record.entry_type.is_extra_time:
                if extra_time >= 0:
                    extra_time = record.worked_hours
            # In any other case, set the extra time to the computed value
            record.extra_time = extra_time

    def compute_day_extra_time(self, hours, theorical_hours):
        extra_time = hours - theorical_hours
        return extra_time

    def compute_day_extra_time_with_factor(self, extra_time, factor):
        extra_time_with_factor = extra_time * factor
        return extra_time_with_factor

    @api.depends('extra_time')
    def _compute_extra_time_with_factor(self):
        for record in self:
            extra_time = record.extra_time
            # Allow negative extra time for extra_time type entries
            if record.entry_type.is_extra_time and extra_time >= 0:
                extra_time = record.worked_hours
            record.extra_time_with_factor = self.compute_day_extra_time_with_factor(
                extra_time,
                record.entry_type.factor
            )

    def compute_compensatory_days(self, month=None):
        """
        Compute compensatory days for the given month.
        If no month is given, it will compute the last month.

        :param month: (int) Month to compute compensatory days for
        
        """
        today = fields.Datetime.now()
        if not month:
            last_month = today - relativedelta(months=1)
            last_month = last_month.replace(day=1)
        else:
            last_month = datetime(year=today.year, month=month, day=1)
        first_day, last_day = monthrange(last_month.year, last_month.month)
        # create a datetime object with the first and last day of the month

        first_check_in = datetime(last_month.year, last_month.month, first_day)
        last_check_in = datetime(last_month.year, last_month.month, last_day)
        
        extra_time = 0
        attendance_records = self.env['hr.attendance'].search([
            ('check_in', '>=', first_check_in),
            ('check_in', '<=', last_check_in),
            ('extra_time', '>', 0)
        ])
        extra_time_by_employee = {}
        for record in attendance_records:
            if record.employee_id.id not in extra_time_by_employee.keys():
                extra_time_by_employee[record.employee_id.id] = {
                    'name': record.employee_id.name,
                    'extra_time': 0,
                    'hours_per_day': record.employee_id.resource_calendar_id.hours_per_day
                }
            extra_time_by_employee[record.employee_id.id]['extra_time'] += record.extra_time_with_factor
        
        for employee in extra_time_by_employee.keys():
            leave_allocation = record.env['hr.leave.allocation'].create({
                'name': 'Compensatory days for %s' % last_month.strftime('%B %Y'),
                'employee_id': employee,
                'holiday_status_id': record.env.ref('hr_holidays.holiday_status_comp').id,
                'number_of_days': extra_time_by_employee[employee]['extra_time']/extra_time_by_employee[employee]['hours_per_day'],
            })
        
            _logger.debug('Compensatory hours for %s: %s', extra_time_by_employee[employee]['name'], extra_time_by_employee[employee]['extra_time'])
            
            

