// Copyright (c) 2023, Rasiin and contributors
// For license information, please see license.txt

frappe.ui.form.on('Send SMS', {
	send_sms: function(frm) {
			// console.log(frm.doc.receiver_list)
			let data= frm.doc.receiver_list
			const lines = data.split('\n');
			const dataArray = lines.map(line => {
			const parts = line.split('-');
			return parts.map(part => part.trim());
			});
			const results = []
			// Step 2: Create an array of objects with name and number properties
			dataArray.map(parts => {
			const name = parts[0];
			const number = parts[1];
			if(name && number){
			results.push({name : name, mobile : number})
			}
			// return { name, number };
			
			});

			// console.log(results);
			if(results){
				// console.log(results)
				results.forEach(e => {
					// alert(e.mobile)
				frappe.call({
					method: "rasiin_hr.rasiin_hr.doctype.send_sms.send_sms.send_sms_all", //dotted path to server method
					args: {
						name: e.name,
						mobile: e.mobile,
						message: frm.doc.message
						// data : Object.assign({}, result)
					},
					callback: function(r) {
						// code snippet
						// console.log(r.message)
					}
				});
				});
		
			}
				
	}
});
