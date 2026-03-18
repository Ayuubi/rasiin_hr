// Copyright (c) 2023, Rasiin and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Confrrmation', {
	// refresh: function(frm) {

	// }
	generate_attendance : function(frm){
		// alert()
		if(!frm.doc.from_date){
			frappe.throw("Please Select From Date")
		}

		if(!frm.doc.to_date){
			frappe.throw("Please Select To Date")
		}

		frappe.call({
			method: "rasiin_hr.api.generate_attendance.generate_attendance", //dotted path to server method
			args : {
				"from_date" : frm.doc.from_date,
				"to_date" : frm.doc.to_date
			},
			callback: function(r) {
				frappe.msgprint("Successfully Generated Attendance")
				// code snippet

			}
		});
	}
});
