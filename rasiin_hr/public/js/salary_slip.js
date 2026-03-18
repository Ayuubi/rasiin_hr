frappe.ui.form.on('Salary Slip', {
	refresh(frm) {
		// your code here
		// alert("okokoko")
	},
	// employee: function(frm){
	// 	let net_pay = frm.doc.net_pay
	//     let data = []
	//     let total =  0
	//     let total_allocate
	//     // let accounts = ["Employee Due - D","Employee Adv - D"]
	// 	let accounts = ["Employee Due - RS","Employee Advances - RS"]
		
	//     accounts.forEach(row=>{
                    		
							

                    
	// 	frappe.call({
	// 		method: "erpnext.accounts.utils.get_balance_on",
	// 		args: {
	// 			company: frappe.defaults.get_user_default("Company"),
	// 			party_type: "Employee",
	// 			party: frm.doc.employee,
	// 			date: frm.doc.posting_date,
	// 			account: row
	// 		},
	// 		callback: function(r, rt) {
	// 			if(r.message) {
	// 			    // console.log(r.message)
	// 			data.push({"account" : row , "due" : Math.abs(r.message), "allocate":  Math.abs(r.message)})
				
	// 			 total += Math.abs(r.message)
	// 			}
				
	// 		}
	// 	});
	//     })
	//     	setTimeout(() => {
	// 		 frm.set_value("employee_advance__and_due" , data)
			 
			
	
	// 		 frm.set_value('total_allocate' , total)
	// 		 frm.set_value('net_pay' , total-Math.abs(frm.doc.rounded_total))
			 

	// 		}, 200);
	   
	// },
    
})

function calculate_total (frm){

	let total_allocate = 0
	var rows = frm.doc.employee_advance__and_due
	rows.forEach(item => {
		total_allocate +=  Math.abs(item.allocate)  
	});
	
	console.log(total_allocate)
	frm.set_value('total_allocate' , total_allocate)
	frm.set_value('net_pay' , Math.abs(frm.doc.rounded_total)-total_allocate)
}

frappe.ui.form.on('Employee Advance  and Due', {
	refresh(frm) {
		
	},
	allocate : function(frm){
		    calculate_total(frm)
		}
})

