// frappe.pages['shift-schedulling'].on_page_load = function(wrapper) {
// 	new ShiftSchedle(wrapper)
// }

// ShiftSchedle = Class.extend(
// 	{
// 		init:function(wrapper){
// 			this.page = frappe.ui.make_app_page({
// 				parent : wrapper,
// 				title: 'Schedule Rotation',
// 				single_column : true
// 			});
// 			this.tbldata = []
			
// 			this.make()
// 			this.create_btns()
// 			this.setup_datatable()
			
// 			this.designation	= []
// 			this.department	= ''
// 			this.year = ''
// 			let days_no = []
// 			let days_name = []
// 			let months_in_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
// 			const d = new Date();
// 			this.monthName =''
// 			// this.curMonth = ''
		
// 		},
// 		make:function(){
// 			let me = this
// 			let months_in_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
// 			const d = new Date();
// 			this.monthName = months_in_year[d.getMonth()];
// 			this.curMonth = this.monthName
		
// 			// alert(me.curMonth)
// 			$(frappe.render_template(frappe.dashbard_page.body, me)).appendTo(me.page.main)




		
// 		},
		
// 		create_btns:function(){
			
// 			let me = this
// 			let field = this.page.add_field({
// 				label: 'Month',
// 				fieldtype: 'Select',
// 				fieldname: 'Month',
// 				options: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
// 				default : me.monthName,
// 				change() {
				
// 					me.curMonth = field.get_value()
// 					me.setup_datatable()
// 				}
// 			});

// 			let desg = this.page.add_field({
// 				label: 'Designation 1',
// 				fieldtype: 'Link',
// 				fieldname: 'desg',
// 				options: "Designation",
			
// 				change() {
// 					me.designation = []
// 					me.designation.push(desg.get_value())
// 					me.designation.push(desg2.get_value())
// 					me.setup_datatable()
// 				}
// 			});
// 			let desg2 = this.page.add_field({
// 				label: 'Designation 2',
// 				fieldtype: 'Link',
// 				fieldname: 'desg2',
// 				options: "Designation",
			
// 				change() {
					
// 					me.designation = []
// 					me.designation.push(desg.get_value())
// 					me.designation.push(desg2.get_value())
// 					me.setup_datatable()
// 				}
// 			});

// 			let depart = this.page.add_field({
// 				label: 'Department',
// 				fieldtype: 'Link',
// 				fieldname: 'dep',
// 				options: "Department",
			
// 				change() {
				
// 					me.department = depart.get_value()
// 					me.setup_datatable()
// 				}
// 			});
// 		},


// 		setup_datatable:function(){
// 			let me = this
// 			let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
// 			let currYear =2024
			
// 			let selMonth = months.indexOf(`${this.curMonth}`)
		
// 			let calander =  showCalendar(selMonth , currYear);
			


// 			// let calander = [
// 			// 	'1 Mon' , '2 Tue' , '3 Wed' , '4 Thu' ,'5 Fr' , 
// 			// 	'6 Mon' , '7 Tue' , '8 Wed' , '9 Thu' ,'10 Fr' ,
// 			// 	'11 Mon' , '12 Tue' , '13 Wed' , '14 Thu' ,'15 Fr',
// 			// 	'16 Mon' , '17 Tue' , '18 Wed' , '19 Thu', '20 Fr' ,
// 			// 	'21 Mon' , '22 Tue' , '23 Wed' , '24 Thu' ,'25 Fr',
// 			// 	'26 Mon' , '27 Tue' , '28 Wed' , '29 Thu' ,'30 Fr' , '31 Fr',
				
				
// 			// 	]
// 				let options = {"":" ", "C":"C","D":"D", "N":"N" , "D & N":"D & N" , "Off" : "Off"}
// 				let columns = [
// 					{formatter:"rowSelection", titleFormatter:"rowSelection",frozen:true , hozAlign:"center", headerSort:false, cellClick:function(e, cell){
// 						cell.getRow().toggleSelect();
// 					  }},
// 					{title : "Name" , field: "employee_name" , frozen:true , headerFilter:"input"}
// 				]
				
// 				calander.forEach( (r , index) => {
// 					// console.log(r.split(" "))
// 					let se_r = r.split(" ")
// 					let mon= ''
// 					if ((selMonth+1)<10){
// 						mon = "0"+(selMonth+1)
// 						// alert()
// 					}
// 					else{
// 						mon=selMonth+1
// 					}
// 					// console.log(mon)
// 				  columns.push(
// 					{
// 						title:se_r[0],
// 						columns : [
// 							{title : se_r[1] , field : `${currYear.toString()}-${(mon).toString()}-${index+1}` , editor:"list", editorParams:{values:options , default:"D"}}
				

// 						]
// 					}
// 					  )
// 				})
// 				console.log(columns)
// 				let datatbl = []
// 				let filters = {}
// 				// if (frappe.user_roles.includes('HR Manager')){
// 				// 	filters = {
// 				// 		status: 'Active',
						
// 				// 	}
// 				// }
// 				// else if (frappe.user_roles.includes('Medical Director')){
// 				// 	filters = {
// 				// 		status: 'Active',
// 				// 		department : "Medical Department - MSH"
						
// 				// 	}
// 				// }
				
// 				// else{
// 				// 	filters = {
// 				// 		status: 'Active',
// 				// 		suppervisor_user : frappe.session.user,
// 				// 		// department : me.department
// 				// 	}
			

// 				// }
			
// 				if(me.designation){
// 					if(me.designation.length > 0){
// 						filters['designation'] = ['in', me.designation]

// 					}
					
// 				}
// 				if(me.department){
// 					// alert(me.department)
// 					filters['department'] = me.department
// 				}
				
// 				// console.log(filters)
// 				filters['status'] = "Active"
// 				frappe.db.get_list('Employee', {
// 					fields: ['employee_name', 'employee' , "name"],
// 					filters: filters,
// 					limit : 1000, 
// 					order_by : 'employee_name'
// 				}).then(records => {
// 					// me.tbldata = records
// 					// console.log(records)
// 					records.forEach(emp => {
// 						frappe.db.get_list(
// 							"Employee Schedulling" , {
// 								filters :{
// 									"employee" : emp.employee,
// 									// "month" : me.curMonth
// 								},
// 								fields :["name" , "shift" , "label"],
// 								limit : 1000, 
// 								order_by : 'employee_name'
// 							}
// 						).then(sch => {
							
// 							let shif_schedule  = {}
// 							shif_schedule['employee'] = emp.name
// 							shif_schedule['employee_name']  = emp.employee_name
// 							// for (const [datakey, datavalue] of Object.entries(sch)) {
// 							// 	shif_schedule[`2023-3-1`] = datavalue.shift
// 							// }
						
// 							sch.forEach(shift_sch => {
// 								if(shift_sch.shift == "Day Shift"){
// 									shift_sch.shift = "D"
// 								}
// 								else if (shift_sch.shift == "Night Shift"){
// 									shift_sch.shift = "N"
// 								}
// 								else if (shift_sch.shift == "Day and Night Shift"){
// 									shift_sch.shift = "D & N"
// 								}
// 								else if (shift_sch.shift == "C"){
// 									shift_sch.shift = "Canteen"
// 								}
// 								else if (shift_sch.shift == "Free"){
// 									shift_sch.shift = "Off"
// 								}
// 								shif_schedule[shift_sch.label] = shift_sch.shift
// 								// shif_schedule['shift'] = shift_sch.shift
							
								
// 							})
							
// 							datatbl.push(shif_schedule)
// 							// shc.push({"employee" : emp.employee})
							
							
// 						})
						

// 					})
				
// 					setTimeout(() => {
// 						// console.log(datatbl)
					
// 						// console.log(datatbl)
// 						console.log(datatbl)
// 						var table = new Tabulator("#schedule", {
// 							height:"380px",
									   
// 							columns: columns,
// 							// frozenRows: 2,
							
							   
							   
							   
// 							data: datatbl
// 							});
// 							let $btn = me.page.set_primary_action('Create Schedule', () => create_schedule(table.getData() ,me.curMonth), 'octicon octicon-plus')
// 							let $btn2 = me.page.set_secondary_action('Print Schedule', () => print_pr(table.getData() , me.curMonth , me.designation), 'octicon octicon-print')
							
// 							// let $btn3 = me.page.set_secondary_action('Excel', () =>  table.download("xlsx", "data.xlsx", {sheetName:"My Data"}))
// 							me.page.clear_custom_actions()
// 							let btn_3 = me.page.add_button(__("Excel"), () => table.download("xlsx", "data.xlsx", {sheetName:"My Data"}), {
// 								icon: "full-page",
// 							});
					
// 						}, 5000);
					

			
			
// 			})
		
			
// 		}

	
	
// 	}

	
// )

// //ceate 
// create_schedule = function(data, curMonth) {
//     frappe.confirm('Are you sure you want to create the schedule?', () => {
//         let scdata = groupBy(data, "employee");
//         let totalDocs = 0;
//         let completedDocs = 0;

//         for (const [key, value] of Object.entries(scdata)) {
//             totalDocs += value.length;

//             value.forEach(innevalue => {
//                 for (const [datakey, datavalue] of Object.entries(innevalue)) {
//                     if (datakey != 'employee_name' && datakey != 'employee') {
//                         if (datavalue) {
//                             let shift = '';

// 							if(datavalue === "D"){
// 								shift = "Day Shift"
// 							}
// 							else if(datavalue === "N"){
// 								shift = "Night Shift"
// 							}
// 							else if(datavalue === "D & N"){
// 								shift = "Day and Night Shift"
// 							}
// 							else if(datavalue === "C"){
// 								shift = "Canteen"
// 							}
// 							else if(datavalue === "Off") {
// 								shift = "Free"
// 							}
//                             let doc_name = `${datakey}-${innevalue.employee}`;

//                             frappe.db.exists("Employee Schedulling", doc_name).then(r => {
//                                 let new_shift = '';

//                                 if (datavalue === "D") {
//                                     new_shift = "Day Shift";
//                                 } else if (datavalue === "N") {
//                                     new_shift = "Night Shift";
//                                 } else if (datavalue === "D & N") {
//                                     new_shift = "Day and Night Shift";
//                                 } else if (datavalue === "C") {
//                                     new_shift = "Canteen";
//                                 } else if (datavalue === "Off") {
//                                     new_shift = "Free";
//                                 }

//                                 if (r) {
//                                     frappe.db.get_doc('Employee Schedulling', doc_name).then(doc => {
//                                         let pr_shift = doc.shift;

//                                         if (pr_shift != new_shift) {
//                                             frappe.db.set_value("Employee Schedulling", doc_name, "shift", new_shift);
//                                         }

//                                         completedDocs++;
//                                         updateProgress();

//                                         // Check if all documents have been processed
//                                         if (completedDocs === totalDocs) {
//                                             // Hide the progress bar and display the success message
//                                             frappe.hide_progress();
//                                             frappe.msgprint("Successfully created schedule");
//                                         }
//                                     });
//                                 } else {
//                                     if (datakey !== "null") {
//                                         let year = new Date().getFullYear();

//                                         frappe.db.insert({
//                                             doctype: 'Employee Schedulling',
//                                             employee: innevalue.employee,
//                                             employee_name: innevalue.employee_name,
//                                             shift: new_shift,
//                                             from_date: frappe.datetime._date(`${datakey}`),
//                                             to_date: frappe.datetime._date(`${datakey}`),
//                                             day: datakey.split('-')[2],
//                                             label: datakey,
//                                             month: curMonth,
//                                             year: year
//                                         }).then(doc => {
//                                             completedDocs++;
//                                             updateProgress();

//                                             // Check if all documents have been processed
//                                             if (completedDocs === totalDocs) {
//                                                 // Hide the progress bar and display the success message
//                                                 frappe.hide_progress();
//                                                 frappe.msgprint("Successfully created schedule");
//                                             }
//                                         });
//                                     }
//                                 }
//                             });
//                         } else {
//                             // frappe.throw(__('No Shift Created'))
//                         }
//                     }
//                 }
//             });
//         }

//         function updateProgress() {
//             let progress = Math.round((completedDocs / totalDocs) * 100);
//             frappe.show_progress(__('Creating Schedule'), progress);
//         }

//         updateProgress();
//     });
// };
// //end create
// function groupBy(objectArray, property) {
// 	return objectArray.reduce((acc, obj) => {
// 	   const key = obj[property];
// 	   if (!acc[key]) {
// 		  acc[key] = [];
// 	   }
// 	   // Add object to list for given key's value
// 	   acc[key].push(obj);
// 	   return acc;
// 	}, {});
//  }
// let days_no = []
// let day_name = []

// print_pr = function(data , curMonth , designation){
// 	if( ! designation.length > 0){
// 		frappe.msgprint("Please Select Designation ")

// 	}
// 	else{
// 		let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
// 		let month_number = months.indexOf(`${curMonth}`)
// 		frappe.call({
// 			method: "rasiin_hr.api.api.get_print_html",
// 			args: {
// 			  data : JSON.stringify(data),
// 			  days : days_no,
// 			  daynames : day_name,
// 			  curMonth : curMonth,
// 			  month_number : month_number+1,
// 			  designation : designation
	
			  
// 			},
// 			callback: function (r) {
// 				//  window.open(response.message);
			  
// 			  var x = window.open();
// 			  x.document.open().write(r.message);
// 			}
// 		  });
// 	}



// }
// function showCalendar(month, year) {

	
// 	days_no = []
// 	day_name = []
// 	var monthDefault = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

// 	var dayDefault = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

// 	// let month = monthDefault;
// 	days = dayDefault;
// 	let calander = []

//     var firstDay = ( new Date( year, month ) ).getDay();

//     var date = 1;
// 	var me = this
//     for ( var i = 0; i < 6; i++ ) {
       
      

        
//         for ( var j = 0; j < 7; j++ ) {
    
//          if (date > daysInMonth(month, year)) {
//                 break;
//             } else {
//                 var d = new Date(year , month , date);
//                 var dayName = days[d.getDay()];
             

// 				calander.push(`${date} ${dayName}`)
// 				days_no.push(date)
// 				day_name.push(dayName)
//                 date++;
			
//             }


//         }

        
//     }
// 	return calander

// }

// function daysInMonth(iMonth, iYear) {
//     return 32 - new Date(iYear, iMonth, 32).getDate();
// }


// let Mybody = `
// <div id="schedule"></div>
// `

// // let body = `

// // <section class="employee__section">
// // <div class="employee__head">
// //   <div class="employee__head__left">
// // 	<h3 class="employee__head__schedule">Shift Schedule</h3>
// // 	<div class="line"></div>
// // 	<h3 class="employee__head__weeks">Week One</h3>
// //   </div>

// //   <div class="employe__head__right">
// // 	<span>For the week of:</span>
// // 	<span>Department Name:</span>
// //   </div>
// // </div>

// // <div class="employee__content">
// //   <div class="employee__content__head">
// // 	<span>Employee</span>
// // 	<span>Sturday</span>
// // 	<span>Sunday</span>
// // 	<span>Monday</span>
// // 	<span>Tuesday</span>
// // 	<span>Wednesday</span>
// // 	<span>Thrusday</span>
// // 	<span>Friday</span>
// //   </div>

// //   <div class="employee__content__sidebar">
// // 	<span>Abdirahmaan Ahmed Hirsi</span>
   
// //   </div>

// //   <div class="employee__content__info">
// //   <div class="employee__content__info__one desc">
// //   <select>
// // 	<option>D</option>
// // 	<option>N</option>
// // 	<option>Free</option>
// //   </select>
// //   <select>
// // 	<option>D</option>
// // 	<option>N</option>
// // 	<option>Free</option>
// //   </select>
// //   <select>
// // 	<option>D</option>
// // 	<option>N</option>
// // 	<option>Free</option>
// //   </select>
// //   <select>
// // 	<option>D</option>
// // 	<option>N</option>
// // 	<option>Free</option>
// //   </select>
// //   <select>
// // 	<option>D</option>
// // 	<option>N</option>
// // 	<option>Free</option>
// //   </select>

// //   <select>
// // 	<option>D</option>
// // 	<option>N</option>
// // 	<option>Free</option>
// //   </select>

// //   <select>
// // 	<option>D</option>
// // 	<option>N</option>
// // 	<option>Free</option>
// //   </select>

  


// // </div>
// //   </div>
// // </div>
// // </section>

// // `
// frappe.dashbard_page = {
// 	body : Mybody
// }
// cash_sales = function(source_name){
// 	frappe.model.open_mapped_doc({
// 		method: "anfac_retail.api.make_invoice.make_sales_invoice",
// 		source_name: source_name
// 	})

// }



frappe.pages['shift-schedulling'].on_page_load = function(wrapper) {
	new ShiftSchedle(wrapper)
}

ShiftSchedle = Class.extend(
	{
		init:function(wrapper){
			this.page = frappe.ui.make_app_page({
				parent : wrapper,
				title: 'Schedule Rotation',
				single_column : true
			});
			this.tbldata = []
			
			this.make()
			this.create_btns()
			this.setup_datatable()
			
			this.designation	= []
			this.department	= ''
			this.year = ''
			let days_no = []
			let days_name = []
			let months_in_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
			const d = new Date();
			this.monthName =''
			// this.curMonth = ''
		
		},
		make:function(){
			let me = this
			let months_in_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
			const d = new Date();
			this.monthName = months_in_year[d.getMonth()];
			this.curMonth = this.monthName
		
			// alert(me.curMonth)
			$(frappe.render_template(frappe.dashbard_page.body, me)).appendTo(me.page.main)




		
		},
		
		create_btns:function(){
			
			let me = this
			let field = this.page.add_field({
				label: 'Month',
				fieldtype: 'Select',
				fieldname: 'Month',
				options: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
				default : me.monthName,
				change() {
				
					me.curMonth = field.get_value()
					me.setup_datatable()
				}
			});

			let desg = this.page.add_field({
				label: 'Designation 1',
				fieldtype: 'Link',
				fieldname: 'desg',
				options: "Designation",
			
				change() {
					me.designation = []
					me.designation.push(desg.get_value())
					me.designation.push(desg2.get_value())
					me.setup_datatable()
				}
			});
			let desg2 = this.page.add_field({
				label: 'Designation 2',
				fieldtype: 'Link',
				fieldname: 'desg2',
				options: "Designation",
			
				change() {
					
					me.designation = []
					me.designation.push(desg.get_value())
					me.designation.push(desg2.get_value())
					me.setup_datatable()
				}
			});

			let depart = this.page.add_field({
				label: 'Department',
				fieldtype: 'Link',
				fieldname: 'dep',
				options: "Department",
			
				change() {
				
					me.department = depart.get_value()
					me.setup_datatable()
				}
			});
		},


		setup_datatable:function(){
			let me = this
			let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
			// let currYear =2025
			let currYear = cint(me.year) || new Date().getFullYear();
			// let currYear = new Date().getFullYear();
			
			let selMonth = months.indexOf(`${this.curMonth}`)
		
			let calander =  showCalendar(selMonth , currYear);
			


			// let calander = [
			// 	'1 Mon' , '2 Tue' , '3 Wed' , '4 Thu' ,'5 Fr' , 
			// 	'6 Mon' , '7 Tue' , '8 Wed' , '9 Thu' ,'10 Fr' ,
			// 	'11 Mon' , '12 Tue' , '13 Wed' , '14 Thu' ,'15 Fr',
			// 	'16 Mon' , '17 Tue' , '18 Wed' , '19 Thu', '20 Fr' ,
			// 	'21 Mon' , '22 Tue' , '23 Wed' , '24 Thu' ,'25 Fr',
			// 	'26 Mon' , '27 Tue' , '28 Wed' , '29 Thu' ,'30 Fr' , '31 Fr',
				
				
			// 	]
				let options = {"":" ", "C":"C","D":"D", "N":"N" , "D & N":"D & N" , "Off" : "Off"}
				let columns = [
					{formatter:"rowSelection", titleFormatter:"rowSelection",frozen:true , hozAlign:"center", headerSort:false, cellClick:function(e, cell){
						cell.getRow().toggleSelect();
					  }},
					{title : "ID" , field: "employee" , frozen:true , headerFilter:"input"},
					{title : "Name" , field: "employee_name" , frozen:true , headerFilter:"input"}
				]
				
				calander.forEach( (r , index) => {
					// console.log(r.split(" "))
					let se_r = r.split(" ")
					let mon= ''
					if ((selMonth+1)<10){
						mon = "0"+(selMonth+1)
						// alert()
					}
					else{
						mon=selMonth+1
					}
					// console.log(mon)
				  columns.push(
					{
						title:se_r[0],
						columns : [
							// {title : se_r[1] , field : `${currYear.toString()}-${(mon).toString()}-${index+1}` , editor:"list", editorParams:{values:options , default:"D"}}
							{title : se_r[1] , field: `${currYear}-${mon}-${String(index+1).padStart(2, "0")}` , editor:"list", editorParams:{values:options , default:"D"}}
				

						]
					}
					  )
				})
				console.log(columns)
				let datatbl = []
				let filters = {}
				// if (frappe.user_roles.includes('HR Manager')){
				// 	filters = {
				// 		status: 'Active',
						
				// 	}
				// }
				// else if (frappe.user_roles.includes('Medical Director')){
				// 	filters = {
				// 		status: 'Active',
				// 		department : "Medical Department - MSH"
						
				// 	}
				// }
				
				// else{
				// 	filters = {
				// 		status: 'Active',
				// 		suppervisor_user : frappe.session.user,
				// 		// department : me.department
				// 	}
			

				// }
			
				if(me.designation){
					if(me.designation.length > 0){
						filters['designation'] = ['in', me.designation]

					}
					
				}
				if(me.department){
					// alert(me.department)
					filters['department'] = me.department
				}
				
				// console.log(filters)
				filters['status'] = "Active"
				frappe.db.get_list('Employee', {
					fields: ['employee_name', 'employee' , "name"],
					filters: filters,
					limit : 1000, 
					order_by : 'employee_name'
				}).then(records => {
					// me.tbldata = records
					// console.log(records)
					records.forEach(emp => {
						frappe.db.get_list(
							"Employee Schedulling" , {
								filters :{
									"employee" : emp.employee,
									// "month" : me.curMonth
									"month": me.curMonth,
									"year": currYear,
								},
								fields :["name" , "shift" , "label"],
								limit : 1000, 
								order_by : 'employee_name'
							}
						).then(sch => {
							
							let shif_schedule  = {}
							shif_schedule['employee'] = emp.name
							shif_schedule['employee_name']  = emp.employee_name
							// for (const [datakey, datavalue] of Object.entries(sch)) {
							// 	shif_schedule[`2023-3-1`] = datavalue.shift
							// }
						
							sch.forEach(shift_sch => {
								if(shift_sch.shift == "Day Shift"){
									shift_sch.shift = "D"
								}
								else if (shift_sch.shift == "Night Shift"){
									shift_sch.shift = "N"
								}
								else if (shift_sch.shift == "Day and Night Shift"){
									shift_sch.shift = "D & N"
								}
								else if (shift_sch.shift == "C"){
									shift_sch.shift = "Canteen"
								}
								else if (shift_sch.shift == "Free"){
									shift_sch.shift = "Off"
								}
								shif_schedule[shift_sch.label] = shift_sch.shift
								// shif_schedule['shift'] = shift_sch.shift
							
								
							})
							
							datatbl.push(shif_schedule)
							// shc.push({"employee" : emp.employee})
							
							
						})
						

					})
				
					setTimeout(() => {
						// console.log(datatbl)
					
						// console.log(datatbl)
						console.log(datatbl)
						var table = new Tabulator("#schedule", {
							height:"380px",
									   
							columns: columns,
							// frozenRows: 2,
							
							   
							   
							   
							data: datatbl
							});
							let $btn = me.page.set_primary_action('Create Schedule', () => create_schedule(table.getData() ,me.curMonth), 'octicon octicon-plus')
							let $btn2 = me.page.set_secondary_action('Print Schedule', () => print_pr(table.getData() , me.curMonth , me.designation), 'octicon octicon-print')
							
							// let $btn3 = me.page.set_secondary_action('Excel', () =>  table.download("xlsx", "data.xlsx", {sheetName:"My Data"}))
							me.page.clear_custom_actions()
							let btn_3 = me.page.add_button(__("Excel"), () => table.download("xlsx", "data.xlsx", {sheetName:"My Data"}), {
								icon: "full-page",
							});
					
						}, 5000);
					

			
			
			})
		
			
		}

	
	
	}

	
)

//ceate 
create_schedule = function(data, curMonth) {
    frappe.confirm('Are you sure you want to create the schedule?', () => {
        let scdata = groupBy(data, "employee");
        let totalDocs = 0;
        let completedDocs = 0;

        for (const [key, value] of Object.entries(scdata)) {
            totalDocs += value.length;

            value.forEach(innevalue => {
                for (const [datakey, datavalue] of Object.entries(innevalue)) {
                    if (datakey != 'employee_name' && datakey != 'employee') {
                        if (datavalue) {
                            let shift = '';

							if(datavalue === "D"){
								shift = "Day Shift"
							}
							else if(datavalue === "N"){
								shift = "Night Shift"
							}
							else if(datavalue === "D & N"){
								shift = "Day and Night Shift"
							}
							else if(datavalue === "C"){
								shift = "Canteen"
							}
							else if(datavalue === "Off") {
								shift = "Free"
							}
                            let doc_name = `${datakey}-${innevalue.employee}`;

                            frappe.db.exists("Employee Schedulling", doc_name).then(r => {
                                let new_shift = '';

                                if (datavalue === "D") {
                                    new_shift = "Day Shift";
                                } else if (datavalue === "N") {
                                    new_shift = "Night Shift";
                                } else if (datavalue === "D & N") {
                                    new_shift = "Day and Night Shift";
                                } else if (datavalue === "C") {
                                    new_shift = "Canteen";
                                } else if (datavalue === "Off") {
                                    new_shift = "Free";
                                }

                                if (r) {
                                    frappe.db.get_doc('Employee Schedulling', doc_name).then(doc => {
                                        let pr_shift = doc.shift;

                                        if (pr_shift != new_shift) {
                                            frappe.db.set_value("Employee Schedulling", doc_name, "shift", new_shift);
                                        }

                                        completedDocs++;
                                        updateProgress();

                                        // Check if all documents have been processed
                                        if (completedDocs === totalDocs) {
                                            // Hide the progress bar and display the success message
                                            frappe.hide_progress();
                                            frappe.msgprint("Successfully created schedule");
                                        }
                                    });
                                } else {
                                    if (datakey !== "null") {
                                        let year = new Date().getFullYear();

                                        frappe.db.insert({
                                            doctype: 'Employee Schedulling',
                                            employee: innevalue.employee,
                                            employee_name: innevalue.employee_name,
                                            shift: new_shift,
                                            from_date: frappe.datetime._date(`${datakey}`),
                                            to_date: frappe.datetime._date(`${datakey}`),
                                            day: datakey.split('-')[2],
                                            label: datakey,
                                            month: curMonth,
                                            year: year
                                        }).then(doc => {
                                            completedDocs++;
                                            updateProgress();

                                            // Check if all documents have been processed
                                            if (completedDocs === totalDocs) {
                                                // Hide the progress bar and display the success message
                                                frappe.hide_progress();
                                                frappe.msgprint("Successfully created schedule");
                                            }
                                        });
                                    }
                                }
                            });
                        } else {
                            // frappe.throw(__('No Shift Created'))
                        }
                    }
                }
            });
        }

        function updateProgress() {
            let progress = Math.round((completedDocs / totalDocs) * 100);
            frappe.show_progress(__('Creating Schedule'), progress);
        }

        updateProgress();
    });
};
//end create
function groupBy(objectArray, property) {
	return objectArray.reduce((acc, obj) => {
	   const key = obj[property];
	   if (!acc[key]) {
		  acc[key] = [];
	   }
	   // Add object to list for given key's value
	   acc[key].push(obj);
	   return acc;
	}, {});
 }
let days_no = []
let day_name = []

print_pr = function(data , curMonth , designation){
	if( ! designation.length > 0){
		frappe.msgprint("Please Select Designation ")

	}
	else{
		let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		let month_number = months.indexOf(`${curMonth}`)
		frappe.call({
			method: "rasiin_hr.api.api.get_print_html",
			args: {
			  data : JSON.stringify(data),
			  days : days_no,
			  daynames : day_name,
			  curMonth : curMonth,
			  month_number : month_number+1,
			  designation : designation
	
			  
			},
			callback: function (r) {
				//  window.open(response.message);
			  
			  var x = window.open();
			  x.document.open().write(r.message);
			}
		  });
	}



}
function showCalendar(month, year) {

	
	days_no = []
	day_name = []
	var monthDefault = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

	var dayDefault = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

	// let month = monthDefault;
	days = dayDefault;
	let calander = []

    var firstDay = ( new Date( year, month ) ).getDay();

    var date = 1;
	var me = this
    for ( var i = 0; i < 6; i++ ) {
       
      

        
        for ( var j = 0; j < 7; j++ ) {
    
         if (date > daysInMonth(month, year)) {
                break;
            } else {
                var d = new Date(year , month , date);
                var dayName = days[d.getDay()];
             

				calander.push(`${date} ${dayName}`)
				days_no.push(date)
				day_name.push(dayName)
                date++;
			
            }


        }

        
    }
	return calander

}

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}


let Mybody = `
<div id="schedule"></div>
`

// let body = `

// <section class="employee__section">
// <div class="employee__head">
//   <div class="employee__head__left">
// 	<h3 class="employee__head__schedule">Shift Schedule</h3>
// 	<div class="line"></div>
// 	<h3 class="employee__head__weeks">Week One</h3>
//   </div>

//   <div class="employe__head__right">
// 	<span>For the week of:</span>
// 	<span>Department Name:</span>
//   </div>
// </div>

// <div class="employee__content">
//   <div class="employee__content__head">
// 	<span>Employee</span>
// 	<span>Sturday</span>
// 	<span>Sunday</span>
// 	<span>Monday</span>
// 	<span>Tuesday</span>
// 	<span>Wednesday</span>
// 	<span>Thrusday</span>
// 	<span>Friday</span>
//   </div>

//   <div class="employee__content__sidebar">
// 	<span>Abdirahmaan Ahmed Hirsi</span>
   
//   </div>

//   <div class="employee__content__info">
//   <div class="employee__content__info__one desc">
//   <select>
// 	<option>D</option>
// 	<option>N</option>
// 	<option>Free</option>
//   </select>
//   <select>
// 	<option>D</option>
// 	<option>N</option>
// 	<option>Free</option>
//   </select>
//   <select>
// 	<option>D</option>
// 	<option>N</option>
// 	<option>Free</option>
//   </select>
//   <select>
// 	<option>D</option>
// 	<option>N</option>
// 	<option>Free</option>
//   </select>
//   <select>
// 	<option>D</option>
// 	<option>N</option>
// 	<option>Free</option>
//   </select>

//   <select>
// 	<option>D</option>
// 	<option>N</option>
// 	<option>Free</option>
//   </select>

//   <select>
// 	<option>D</option>
// 	<option>N</option>
// 	<option>Free</option>
//   </select>

  


// </div>
//   </div>
// </div>
// </section>

// `
frappe.dashbard_page = {
	body : Mybody
}
cash_sales = function(source_name){
	frappe.model.open_mapped_doc({
		method: "anfac_retail.api.make_invoice.make_sales_invoice",
		source_name: source_name
	})

}