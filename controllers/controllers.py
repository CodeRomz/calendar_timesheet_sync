# -*- coding: utf-8 -*-
# from odoo import http


# class CalendarTimesheetSync(http.Controller):
#     @http.route('/calendar_timesheet_sync/calendar_timesheet_sync', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/calendar_timesheet_sync/calendar_timesheet_sync/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('calendar_timesheet_sync.listing', {
#             'root': '/calendar_timesheet_sync/calendar_timesheet_sync',
#             'objects': http.request.env['calendar_timesheet_sync.calendar_timesheet_sync'].search([]),
#         })

#     @http.route('/calendar_timesheet_sync/calendar_timesheet_sync/objects/<model("calendar_timesheet_sync.calendar_timesheet_sync"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('calendar_timesheet_sync.object', {
#             'object': obj
#         })

