from . import __version__ as app_version

app_name = "rasiin_hr"
app_title = "Rasiin Hr"
app_publisher = "Rasiin"
app_description = "HR for Rasiin"
app_email = "rasiinllc@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "https://unpkg.com/tabulator-tables//dist/css/tabulator_simple.min.css"
# app_include_js = ["https://unpkg.com/tabulator-tables/dist/js/tabulator.min.js" , "https://oss.sheetjs.com/sheetjs/xlsx.full.min.js","/assets/rasiin_hr/js/query_report.js"]

# include js, css files in header of web template
# web_include_css = "/assets/rasiin_hr/css/rasiin_hr.css"
# web_include_js = "/assets/rasiin_hr/js/rasiin_hr.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "rasiin_hr/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Salary Slip" : "public/js/salary_slip.js"}
doctype_list_js = {"Employee" : "public/js/employee_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "rasiin_hr.utils.jinja_methods",
#	"filters": "rasiin_hr.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "rasiin_hr.install.before_install"
# after_install = "rasiin_hr.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "rasiin_hr.uninstall.before_uninstall"
# after_uninstall = "rasiin_hr.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "rasiin_hr.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Shift Type": "rasiin_hr.overides.shift_type.CustomShiftType",
    "Payroll Entry" : "rasiin_hr.overides.payroll_entry.PayrollEntry",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "Employee Checkin": {
	# 	"before_insert": "rasiin_hr.api.api.create_attendance",
		
	# },
    # "Employee": {
	# 	"after_insert": "rasiin_hr.api.create_emp_on_device.synchronize_employees",
		
	# },
	"Salary Slip" :{
		"before_submit": "rasiin_hr.api.inc_dec_salary.inc_dec_salary"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
       "cron": {
	"* 12 * * *": [
		# "rasiin_hr.api.submit_attendace.mark_attendance_leaves",
        "rasiin_hr.api.submit_attendace.submit_attendance"
        

		
	],
    # "* 07 * * *": [
	# 	# "rasiin_hr.api.submit_attendace.mark_attendance_leaves",
    #     "rasiin_hr.api.leave_assigment_bulk_sms.send_bulk_sms"
        

		
	# ],
	   }
	# "daily": [
	# 	"rasiin_hr.tasks.daily"
	# ],
	# "hourly": [
	# 	"rasiin_hr.tasks.hourly"
	# ],
	# "weekly": [
	# 	"rasiin_hr.tasks.weekly"
	# ],
	# "monthly": [
	# 	"rasiin_hr.tasks.monthly"
	# ],
}

# Client and Server Script Fixtures
fixtures = [
    {
        "doctype": doctype,
        "filters": [["module", "=", "Rasiin Hr"]]
    }
    for doctype in [
        "Client Script",
        "Server Script",
        "Custom Field",
        "Print Format",
        # "Home Page"  # Uncomment if needed
    ]
] + [
    # {"doctype": "Role Profile"}

]

# Testing
# -------

# before_tests = "rasiin_hr.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "rasiin_hr.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "rasiin_hr.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"rasiin_hr.auth.validate"
# ]
