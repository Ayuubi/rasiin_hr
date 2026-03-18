frappe.ui.form.on('Employees Commission', {
    refresh(frm) {
		frm.set_query('employee', function(doc) {
			return {
				filters: {
                    "status": "Active"
				}
			};
		});
		frm.set_query('component', function(doc) {
			return {
				filters: {
					"type": "Earning",
				}
			};
		});
        if (!frm.doc.from_date) {
            let today = frappe.datetime.get_today();
            let first_day = today.slice(0, 8) + "01";
            frm.set_value("from_date", first_day);
        }
    },

    employee_type: function(frm) {
		if (frm.doc.employee_type == "Employee"){
			update_commission_details(frm);
		}

		if (frm.doc.employee_type == "Doctor"){
			doctor_update_commission_details(frm);
		}
    },

    from_date: function(frm) {
        if (frm.doc.employee_type === "Employee") {
            update_commission_details(frm);
        }
    },

    to_date: function(frm) {
        if (frm.doc.employee_type === "Employee") {
            update_commission_details(frm);
        }
    },

    department: function(frm) {
        if (frm.doc.employee_type === "Employee") {
            update_commission_details(frm);
        }
    },

employee: function(frm) {
    if (frm.doc.employee_type === "Employee") {
        if (frm.doc.employee) {
            update_commission_detail_individual_employee(frm);
        } else {
            update_commission_details(frm);
        }
    } else if (frm.doc.employee_type === "Doctor") {
        if (frm.doc.employee) {
            update_commission_detail_individual_doctor(frm);
        } else {
            doctor_update_commission_details(frm);
        }
    }
},

	

    before_save(frm) {
        calculate_totals(frm);
    },
	
	
});
frappe.ui.form.on('Commission Payments', {
    payment(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.balance = Number(row.amount.toFixed(2)) - Number(row.payment.toFixed(2));

        // Update totals when any payment changes
        let total_amount = 0;
        let total_payment = 0;

        frm.doc.commission_payments.forEach(child => {
            total_amount += Number(child.amount.toFixed(2)) || 0;
            total_payment += Number(child.payment.toFixed(2)) || 0;
        });

        frm.doc.total_amount = total_amount;
        frm.doc.total_payment = total_payment;

        frm.refresh_field('commission_payments');
        frm.refresh_field('total_amount');
        frm.refresh_field('total_payment');
    }
})

function update_commission_details(frm) {
    if (!frm.doc.from_date || !frm.doc.to_date) {
        return;
    }

    const filters = {
        from_date: frm.doc.from_date,
        to_date: frm.doc.to_date,
        department: frm.doc.department || ''
    };

    frappe.call({
        method: "rasiin_hr.rasiin_hr.doctype.employees_commission.employees_commission.employee_commision",
        args: filters,
        callback: function(r) {
            if (r.message) {
                frm.clear_table("commission_payments");

                let total_amount = 0;
                let total_payment = 0;

                r.message.forEach(res => {
                    let child = frm.add_child("commission_payments");
                    child.employee = res.employee;
                    child.employee_name = res.employee_name;
                    child.amount = Number(res.amount.toFixed(2)) || 0;
                    child.payment = Number(res.amount.toFixed(2)) || 0;
                    child.balance = child.amount - child.payment;

                    total_amount += child.amount;
                    total_payment += child.payment;
                });

                frm.set_value("total_amount", total_amount);
                frm.set_value("total_payment", total_payment);

                frm.refresh_fields(["commission_payments", "total_amount", "total_payment"]);
            }
        }
    });
}

function update_commission_detail_individual_employee(frm) {
    if (!frm.doc.from_date || !frm.doc.to_date || !frm.doc.employee) {
        return;
    }

    const filters = {
        from_date: frm.doc.from_date,
        to_date: frm.doc.to_date,
        department: frm.doc.department || ''
    };

    frappe.call({
        method: "rasiin_hr.rasiin_hr.doctype.employees_commission.employees_commission.employee_commision",
        args: filters,
        callback: function(r) {
            if (r.message) {
                frm.clear_table("commission_payments");

                let total_amount = 0;
                let total_payment = 0;

                r.message.forEach(res => {
                    if (res.employee == frm.doc.employee) {
                        let child = frm.add_child("commission_payments");
                        child.employee = res.employee;
                        child.employee_name = res.employee_name;
                        child.amount = Number(res.amount.toFixed(2)) || 0;
                        child.payment = Number(res.amount.toFixed(2)) || 0;
                        child.balance = child.amount - child.payment;

                        total_amount += child.amount;
                        total_payment += child.payment;
                    }

					
                });

                frm.set_value("total_amount", total_amount);
                frm.set_value("total_payment", total_payment);

                frm.refresh_fields(["commission_payments", "total_amount", "total_payment"]);
            }
        }
    });
}
function calculate_totals(frm) {
    let total_amount = 0;
    let total_payment = 0;

    frm.doc.commission_payments.forEach(row => {
        total_amount += flt(row.amount || 0);
        total_payment += flt(row.payment || 0);
    });

    frm.set_value("total_amount", total_amount);
    frm.set_value("total_payment", total_payment);
}

function doctor_update_commission_details(frm) {
    if (!frm.doc.from_date || !frm.doc.to_date) {
        return;
    }

    const filters = {
        from_date: frm.doc.from_date,
        to_date: frm.doc.to_date,
        department: frm.doc.department || ''
    };

    frappe.call({
        method: "rasiin_hr.rasiin_hr.doctype.employees_commission.employees_commission.doctor_commision",
        args: filters,
        callback: function(r) {
            if (r.message) {
                frm.clear_table("commission_payments");

                let total_amount = 0;
                let total_payment = 0;

                r.message.forEach(res => {
                    let child = frm.add_child("commission_payments");
                    child.employee = res.employee;
                    child.employee_name = res.employee_name;
                    child.amount = Number(res.amount.toFixed(2)) || 0;
                    child.payment = Number(res.amount.toFixed(2)) || 0;
                    child.balance = child.amount - child.payment;

                    total_amount += child.amount;
                    total_payment += child.payment;
                });

                frm.set_value("total_amount", total_amount);
                frm.set_value("total_payment", total_payment);

                frm.refresh_fields(["commission_payments", "total_amount", "total_payment"]);
            }
        }
    });
}

function update_commission_detail_individual_doctor(frm) {
    if (!frm.doc.from_date || !frm.doc.to_date || !frm.doc.employee) {
        return;
    }

    const filters = {
        from_date: frm.doc.from_date,
        to_date: frm.doc.to_date,
        department: frm.doc.department || ''
    };

    frappe.call({
        method: "rasiin_hr.rasiin_hr.doctype.employees_commission.employees_commission.doctor_commision",
        args: filters,
        callback: function(r) {
            if (r.message) {
                frm.clear_table("commission_payments");

                let total_amount = 0;
                let total_payment = 0;

                r.message.forEach(res => {
                    if (res.employee == frm.doc.employee) {
                        let child = frm.add_child("commission_payments");
                        child.employee = res.employee;
                        child.employee_name = res.employee_name;
                        child.amount = Number(res.amount.toFixed(2)) || 0;
                        child.payment = Number(res.amount.toFixed(2)) || 0;
                        child.balance = child.amount - child.payment;

                        total_amount += child.amount;
                        total_payment += child.payment;
                    }

					
                });

                frm.set_value("total_amount", total_amount);
                frm.set_value("total_payment", total_payment);

                frm.refresh_fields(["commission_payments", "total_amount", "total_payment"]);
            }
        }
    });
}