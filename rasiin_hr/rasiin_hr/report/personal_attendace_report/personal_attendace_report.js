// Copyright (c) 2023, Rasiin and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Personal Attendace Report"] = {
	"filters": [
		
			{
				fieldname: "from_date",
				label: __("From Date"),
				fieldtype: "Date",
				default:frappe.datetime.now_date(),
				reqd: 1
			},
			{
				fieldname: "to_date",
				label: __("To Date"),
				fieldtype: "Date",
				default:frappe.datetime.now_date(),
				reqd: 1
			},
			{
				fieldname: "employee",
				label: __("Employee"),
				fieldtype: "Link",
				options: "Employee",
				on_change: function() {
					frappe.db.get_value("Employee" , frappe.query_report.get_filter_value("employee") , "employee_name")
		.then(res => {
			// console.log(res)
			let emp_name = res.message.employee_name
			frappe.query_report.set_filter_value('employee_name', emp_name);
			
		})
						} 
				
				// default:frappe.datetime.now_date(),
				// reqd: 1
			},
			{
				fieldname: "employee_name",
				label: __("Employee Name"),
				fieldtype: "Data",
				read_only : 1,
				fetch_from: "get_cities",
				// default:frappe.datetime.now_date(),
				// reqd: 1
			},
			{
				fieldname: "worked_on_holiday",
				label: __("Worked On Holiday"),
				fieldtype: "Check",
				default:0,
				
			},

	],

	formatter: function(value, row, column, data, default_formatter) {
		// console.log(default_formatter)
		value = default_formatter(value, row, column, data);
		// const summarized_view = frappe.query_report.get_filter_value('summarized_view');
		// const group_by = frappe.query_report.get_filter_value('group_by');

		
				if (value == 'Present' )
					value = "<span style='color:green' >" + value + "</span>";
				else if (value == 'Absent')
					value = "<span style='color:red'>" + value + "</span>";
				else if (value == 'Half Day')
					value = "<span style='color:orange'>" + value + "</span>";
				else if (value == 'On Leave')
					value = "<span style='color:#318AD8'>" + value + "</span>";
				// else if (value == 'Holiday')
				// 	value = "<span style='color:yellow'>" + value + "</span>";
			
		

		return value;
	},
	custformatter: function(value, row, column, data, default_formatter) {
		// console.log(default_formatter)
		// value = default_formatter(value, row, column, data);
		// const summarized_view = frappe.query_report.get_filter_value('summarized_view');
		// const group_by = frappe.query_report.get_filter_value('group_by');

		
				if (value == 'Present' )
					value = "<span style='color:green' >" + value + "</span>";
				else if (value == 'Absent')
					value = "<span style='color:red'>" + value + "</span>";
				else if (value == 'Half Day')
					value = "<span style='color:orange'>" + value + "</span>";
				else if (value == 'On Leave')
					value = "<span style='color:#318AD8'>" + value + "</span>";
				// else if (value == 'Holiday')
				// 	value = "<span style='color:yellow'>" + value + "</span>";
			
		

		return value;
	},
	getEmpoyeeName: function(employee) {
		let emp_name = ""
		alert()
		frappe.db.get_value("Employee" , employee , "employee_name")
		.then(res => {
			// console.log(res)
			emp_name = res.message.employee_name
		})

			return emp_name
		
		

		

		
	}
	
};


