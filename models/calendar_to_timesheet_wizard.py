from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

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

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.task_id and self.task_id.project_id != self.project_id:
            self.task_id = False

    def action_log_time(self):
        self.ensure_one()
        if self.duration <= 0:
            raise ValidationError(_("Duration must be greater than zero."))

        # ✅ Access duration limits from project_id (not task)
        if self.task_id and self.task_id.project_id:
            project = self.task_id.project_id
            if project.use_timesheet_control:
                min_duration = (project.min_time or 0.0) / 60.0
                max_duration = (project.max_time or 0.0) / 60.0

                if min_duration and self.duration < min_duration:
                    raise ValidationError(_(
                        "Duration is below the minimum allowed (%.2f h) for this project.") % min_duration)
                if max_duration and self.duration > max_duration:
                    raise ValidationError(_(
                        "Duration exceeds the maximum allowed (%.2f h) for this project.") % max_duration)

        # ✅ Create analytic line
        self.env['account.analytic.line'].create({
            'name': self.name,
            'date': self.date_time_start.date(),
            'unit_amount': self.duration,
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.env.user.employee_id.id,
        })

        # ✅ Update calendar event flag
        if self.event_id:
            self.event_id.is_timesheet_logged = True
