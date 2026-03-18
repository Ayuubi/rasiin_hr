frappe.ui.form.on('Salary Payments', {
    before_save(frm) {
        validate_missing_values(frm)
        let total_amount = 0;
        let total_payment = 0;

        frm.doc.salary_payments_details.forEach(row => {
            total_amount += flt(row.amount);
            total_payment += flt(row.payment);
        });

        frm.set_value('total_amount', total_amount);
        frm.set_value('total_payment', total_payment);

        frm.refresh_field('total_amount');
        frm.refresh_field('total_payment');
    },
    refresh(frm) {
        // update_salary_details(frm)
        
        frm.set_query("account", function() {
            return {
                filters: {
                    account_type: ["in", ["Bank", "Cash"]]
                }
            };
        });
        
        if (frm.is_new()){
             update_salary_details(frm)
        }
        if (!frm.doc.from_date) {
            let today = frappe.datetime.get_today();
            let first_day = today.slice(0, 8) + "01";
            frm.set_value("from_date", first_day);
        } 
    },

    from_date: update_salary_details,
    to_date: update_salary_details,
    department: update_salary_details
});

function validate_missing_values(frm) {
    
    let total_amount = 0;
    frm.doc.salary_payments_details.forEach(detailRow => {
        // console.log(detailRow)
        if (!detailRow.amount){
        const filters = {
            // start_date: frm.doc.from_date,
            // end_date: frm.doc.to_date,
            name: detailRow.salary_slip,
            docstatus: 1,
            employee: detailRow.employee
        };

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Salary Slip",
                filters: filters,

                fields: ["net_pay", "paid_amount", "name"],
                page_length: 1000  // alternative to limit

            },
            callback: function (response) {
           
                if (response && response.message.length) {
                    response.message.forEach(function (slip) {
                        
                        let unpaid = slip.net_pay - slip.paid_amount;
                         unpaid = Number(unpaid.toFixed(2)); // ✅ round it immediately
                        
                       
                        if (unpaid !== 0) {
                            // Update the matching child row
                            const child = frm.doc.salary_payments_details.find(r => r.employee === detailRow.employee);
                            if (child) {
                                child.amount = unpaid;
                                child.balance = Number((unpaid - (child.payment || 0)).toFixed(2));
                                total_amount= total_amount + unpaid
                            }
                        }
                    });
                    frm.doc.total_amount = total_amount;
                    frm.refresh_field("salary_payments_details");
                    frm.refresh_field("total_amount");
                }
            }
        
        });
    }
    });
}

function update_salary_details(frm) {
    if (frm.doc.from_date && frm.doc.to_date) {
        const filters = {
            start_date: frm.doc.from_date,
            end_date: frm.doc.to_date,
            docstatus: 1
        };

        if (frm.doc.department) {
            filters.department = frm.doc.department;
        }

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Salary Slip",
                filters: filters,
                fields: ["*"],
                limit_page_length: 1000 
            },
            callback: function (response) {
                if (response.message) {
                    frm.clear_table("salary_payments_details");

                    let total_amount = 0;
                    let total_payment = 0;
                    let payroll_entry='';

                    response.message.forEach(function (row) {
                        let unpaid = row.net_pay - row.paid_amount;
                         unpaid = Number(unpaid.toFixed(2)); // ✅ round it immediately
                        console.log(row)
                        if (unpaid !== 0) {
                            let child = frm.add_child("salary_payments_details");
                            child.employee = row.employee;
                            child.employee_name = row.employee_name;
                            child.department = row.department;
                            child.amount = unpaid;
                            child.payment = unpaid;
                            child.balance = 0;
                            child.salary_slip = row.name;
                            child.payroll_entry = row.payroll_entry;
                            payroll_entry= row.payroll_entry;
                            

                            total_amount += unpaid;
                            total_payment += unpaid;
                        }
                    });

                    frm.doc.total_amount = total_amount;
                    frm.doc.total_payment = total_payment;
                    frm.doc.payroll_entry = payroll_entry;
                    
                    frm.refresh_field("salary_payments_details");
                    frm.refresh_field("total_amount");
                    frm.refresh_field("total_payment");
                    frm.refresh_field("payroll_entry");
                }
            }
        });
    }
}

frappe.ui.form.on('Salary Payments Details', {
    payment(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.balance = row.amount - row.payment;

        // Update totals when any payment changes
        let total_amount = 0;
        let total_payment = 0;

        frm.doc.salary_payments_details.forEach(child => {
            total_amount += child.amount || 0;
            total_payment += child.payment || 0;
        });

        frm.doc.total_amount = total_amount;
        frm.doc.total_payment = total_payment;

        frm.refresh_field('salary_payments_details');
        frm.refresh_field('total_amount');
        frm.refresh_field('total_payment');
    }
})
