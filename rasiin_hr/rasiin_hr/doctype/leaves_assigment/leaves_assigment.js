frappe.ui.form.on('Leaves Assigment', {
	refresh(frm) {
		// your code here
		if(frm.doc.docstatus == 0){
		frm.add_custom_button(__("Reject"), function() {
			frm.set_value("status" , "Rejected")
			frm.savesubmit()
			// frappe.db.set_value("Nofication" , frm.doc.notication,'seen' , "1")
			// frappe.db.set_value('Nofication', frm.doc.notication, 'seen', 1)
    .then(r => {
        let doc = r.message;
        console.log(doc);
    })

		})
	}
		
	},
	leave_type:function(frm){  
    
			frappe.call({
				method: "rasiin_hr.rasiin_hr.doctype.leaves_assigment.leaves_assigment.get_last_leave",
				args: { 
				  doc: "Leaves Assigment",
				  docname:frm.doc.employee
				  
				},
				callback: function(r) {
					// alert("ok")
				    // console.log(r)
					// alert("ok")
				if (r.message){
					
				frappe.msgprint(`The Last Leave Type of  <b>${frm.doc.employee_name} </b> was <b>${r.message.leave_type}</b> Ended  <b>${r.message.to_date} </b>`)
				}
				
				  
				}
			  });
		
	
	         
}
})