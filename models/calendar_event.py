from odoo import models, fields, api, _
from odoo.exceptions import AccessError

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    is_timesheet_logged = fields.Boolean(
        string="Timesheet Logged",
        readonly=True,
        help="Indicates whether this event has been logged into timesheet."
    )

    def action_open_calendar_timesheet_wizard(self):
        self.ensure_one()
        if not self.env.user.has_group('hr_timesheet.group_hr_timesheet_user'):
            raise AccessError(_("You are not allowed to log timesheets."))

        return {
            'type': 'ir.actions.act_window',
            'name': _('Log Time from Event'),
            'res_model': 'calendar.to.timesheet.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': self.name,
                'default_date_time_start': self.start,
                'default_date_time_end': self.stop,
                'default_event_id': self.id,
            },
        }
