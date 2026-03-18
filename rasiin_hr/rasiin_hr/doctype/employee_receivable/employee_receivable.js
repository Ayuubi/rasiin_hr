// Copyright (c) 2024, Rasiin and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Receivable', {
	refresh: function (frm) {


		if (frm.doc.docstatus == 1) {

			frm.add_custom_button(__("Deduction from Salary"), function () {
				frm.events.make_deduction_via_additional_salary(frm);
			});
		}
	},
	employee: function (frm) {

		frappe.call({
			// 		method: "erpnext.accounts.utils.get_balance_on",
			method: "erpnext.accounts.utils.get_balance_on",
			args: {
				date: get_today(),
				party_type: 'Employee',
				party: frm.doc.employee,
				account: frm.doc.account

			},
			callback: function (r) {
				// 			doc.outstanding_balance = format_currency(r.message, erpnext.get_currency(doc.company));
				frm.set_value("balance", r.message)
				// 			refresh_field('outstanding_balance', 'accounts');
			}
		})
	},

	// frm.events.make_deduction_via_additional_salary(frm);


	make_deduction_via_additional_salary: function (frm) {
		frappe.call({
			method: "rasiin_hr.rasiin_hr.doctype.employee_receivable.employee_receivable.create_return_through_additional_salary",
			args: {
				doc: frm.doc
			},
			callback: function (r) {
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		});
	},
});
