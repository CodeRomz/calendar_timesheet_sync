from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CalendarToTimesheetWizard(models.TransientModel):
    _name = 'calendar.to.timesheet.wizard'
    _description = 'Wizard to Log Calendar Events to Timesheets'

    name = fields.Char(string="Description", required=True)
    date_time_start = fields.Datetime(string="Start", required=True)
    date_time_end = fields.Datetime(string="End", required=True)
    duration = fields.Float(string="Duration (Hours)", compute='_compute_duration', store=True)
    project_id = fields.Many2one('project.project', string="Project", required=True)
    task_id = fields.Many2one('project.task', string="Task", domain="[('project_id', '=', project_id)]")
    event_id = fields.Many2one('calendar.event', string="Calendar Event", readonly=True)

    @api.depends('date_time_start', 'date_time_end')
    def _compute_duration(self):
        for rec in self:
            if rec.date_time_start and rec.date_time_end:
                delta = rec.date_time_end - rec.date_time_start
                rec.duration = round(delta.total_seconds() / 3600.0, 2)
            else:
                rec.duration = 0.0

    def action_log_time(self):
        self.ensure_one()

        if self.duration <= 0:
            raise ValidationError(_("Duration must be greater than zero."))

        self.env['account.analytic.line'].create({
            'name': self.name,
            'date_time': self.date_time_start,  # Start time (datetime)
            'unit_amount': self.duration,
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.env.user.employee_id.id,
        })

        if self.event_id:
            self.event_id.is_timesheet_logged = True


