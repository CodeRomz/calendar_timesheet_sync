# calendar_timesheet_sync/models/calendar_event.py
from odoo import api, models, _
from odoo.exceptions import UserError

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    def action_open_timesheet_calendar_wizard(self):
        self.ensure_one()
        if not self.start or not self.stop:
            raise UserError(_("A start and end time must be set on the calendar event."))

        view_id = self.env.ref('hr_timesheet_calendar.view_hr_timesheet_calendar_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': _('Add in Timesheet'),
            'res_model': 'hr.timesheet.calendar.wizard',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'context': {
                'default_name': self.name,
                'default_date_time_start': self.start,
                'default_date_time_end': self.stop,
            },
        }
