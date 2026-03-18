

frappe.pages['weakly-schedule'].on_page_load = function(wrapper) {
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
			this.from_date	= get_today()
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
			// let field = this.page.add_field({
			// 	label: 'Month',
			// 	fieldtype: 'Select',
			// 	fieldname: 'Month',
			// 	options: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
			// 	default : me.monthName,
			// 	change() {
				
			// 		me.curMonth = field.get_value()
			// 		me.setup_datatable()
			// 	}
			// });

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
			let currYear = new Date().getFullYear();
			
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
				let options = {"Day Shift":"Day Shift", "Night Shift":"Night Shift" , "Free" : "Free"}
				let columns = [
					{title : "Name" , field: "employee_name" , frozen:true , headerFilter:"input"}
				]
				
				calander.forEach( (r , index) => {
				  columns.push(
					{title : r , field : r.toLowerCase() , editor:"list", editorParams:{values:options , default:"Day Shift"}}
				  )
				})
				let datatbl = []
				let filters = {}
				if (frappe.user_roles.includes('HR Manager')){
					filters = {
						status: 'Active',
						
					}
				}
				else if (frappe.user_roles.includes('Medical Director')){
					filters = {
						status: 'Active',
						department : "Medical Department - RS"
						
					}
				}
				
				else{
					filters = {
						status: 'Active',
						suppervisor_user : frappe.session.user,
						// department : me.department
					}
			

				}
				
				if(me.designation){
						
					filters['designation'] = ['in', me.designation]
				}
				if(me.department){
						
					filters['department'] = me.department
				}
				
			
				frappe.db.get_list('Employee', {
					fields: ['employee_name', 'employee' , "name"],
					filters: filters,
					limit : 1000, 
					order_by : 'employee_name'
				}).then(records => {
					// me.tbldata = records
					
					records.forEach(emp => {
						frappe.db.get_list(
							"Weakly Employee Schedule" , {
								filters :{
									"employee" : emp.employee,
									// "month" : me.curMonth
								},
								fields :["name" , "shift" , "label" ,'day'],
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
						var table = new Tabulator("#schedule", {
							height:"380px",
									   
							columns: columns,
							// frozenRows: 2,
							   
							   
							   
							data: datatbl
							});
							let $btn = me.page.set_primary_action('Create Schedule', () => create_schedule(table.getData() ,me.curMonth , me.from_date), 'octicon octicon-plus')
							let $btn2 = me.page.set_secondary_action('Print Schedule', () => print_pr(table.getData() , me.curMonth , me.designation), 'octicon octicon-print')
							
						
					}, 5000);
					

			
			
			})
		
			
		}

	
	
	}

	
)


create_schedule =function(data , curMonth ,from_date){

	// alert("ok ok ")
// let monthNo = curMonth
// console.log(data)
var shift = ''
frappe.confirm('Are you sure you create schedule?',
    () => {
		let scdata = groupBy(data , "employee")
		console.log("this is " , scdata)

let ind = 0
for (const [key, value] of Object.entries(scdata)) {
	let year = new Date().getFullYear()
	console.log("this value" , value)
		var totalDocs = value.length;
		var completedDocs  = 0

	value.forEach(innevalue =>{
		
		for (const [datakey, datavalue] of Object.entries(innevalue)) {
			if(datakey  != 'employee_name' && datakey != 'employee' ){
			ind += 1
			if(datavalue ){
			
				let doc_name = `${datakey}-${innevalue.employee}`
				// console.log("out" , shift)
				// console.log(innevalue.employee)
				frappe.db.exists("Weakly Employee Schedule" , doc_name).then(r => {
					// console.log(r)
					let new_shift = datavalue
					
					
					if(r){
						frappe.db.get_doc('Weakly Employee Schedule', doc_name)
								.then(doc => {
									let pr_shif = doc.shift
									// frappe.db.get_value("Employee Schedulling" , doc_name , "shift").then(pr_shif => {
										// console.log("in" , new_shift)
										if(pr_shif != new_shift){
											// alert(shift)
								frappe.db.set_value("Employee Schedulling" , doc_name,"shift" , new_shift)
										}
									
								})
						

					}else{

						if(datakey !== "null" ){
						
						 
            
            // Publish progress update
           				
						// alert(datakey)
						frappe.db.insert({
							doctype: 'Weakly Employee Schedule',
							employee: innevalue.employee,
							employee_name : innevalue.employee_name,
							shift : new_shift,
							from_date : frappe.datetime._date(`${from_date}`),
							to_date : frappe.datetime._date(`${from_date}`),
							day: ind,
							label : datakey,
							month : curMonth,
							year : year
					}).then(doc => {
						// alert("done")
						completedDocs += 1
						let progress = Math.round((completedDocs / totalDocs) * 100);
						// frappe.show_progress('Creating Schedle..', completedDocs, totalDocs, 'Please wait');
						
						
					})

					}
				}
				
				})
	
}}
else{
	// frappe.throw(__('No Shift Created'))
}

		}
	})
	// value.forEach(row => {
	
	// })

  }
frappe.msgprint("Seccesfuly Created Schedule")


        // action to perform if Yes is selected

    }, () => {
        // action to perform if No is selected
    })


}

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
	if( ! designation){
		frappe.msgprint("Please Select Designation ")

	}
	else{
		let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		let month_number = months.indexOf(`${curMonth}`)
		frappe.call({
			method: "rasiin_hr.api.api.get_print_html_weaky",
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

    // var firstDay = ( new Date( year, month ) ).getDay();

    var date = 1;
	var me = this
    for ( var i = 0; i < 7; i++ ) {
       
      

        
        // for ( var j = 0; j < 7; j++ ) {
    
       
                var d = new Date(year , month , date);
                var dayName = days[d.getDay()];
             

				calander.push(`${dayName}`)
				days_no.push(date)
				day_name.push(dayName)
                date++;
			
           


        // }

        
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