# __manifest__.py
{
    'name': 'Calendar Timesheet Sync',
    'version': '17.0.1.0.0',
    'category': 'Tools',
    'summary': 'Log calendar events into timesheet using the OCA calendar wizard',
    'description': """
Integrates calendar.event with the OCA hr_timesheet_calendar wizard.
Adds a button on calendar events to log time in the wizard with default values.
""",
    'author': 'CodeRomz',
    'license': 'AGPL-3',
    'depends': [
        'calendar',
        'hr_timesheet_calendar',
        'project_timesheet_time_control',
    ],
    'data': [
        'views/calendar_event_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
