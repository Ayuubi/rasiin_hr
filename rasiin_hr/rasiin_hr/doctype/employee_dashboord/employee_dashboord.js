// Copyright (c) 2023, Rasiin and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Dashboord', {
	// refresh: function(frm) {

// Copyright (c) 2023, Rasiin Tech and contributors
// For license information, please see license.txt





	refresh: function(frm) {
		
	  
			// frm.set_df_property('view_as_chart', 'css_class', 'align-right');
		
			$('.indicator-pill').hide()
		// $('.standard-actions').hide()
		// frm.disable_save();

	
		
		get_history("employee")

		var tabs = $('.form-tabs');
		var parentElement = $('.parent');

// Get all child elements of the parent
		var childElements = tabs.children();

		// Loop through each child element and attach click event handler
		childElements.each(function() {
		var childElement = $(this);
		var tab = childElement[0].innerText.replace(/ /g, '_').toLowerCase()
		
		// Attach click event handler to the current child element
		childElement.click(function() {
			// alert(tab)
			get_history(tab)
			// Code to execute when the current child element is clicked
			// ...
		});
		});

		// $('#patient-history-vitals_tab-tab').on('click', function() {
        //     // Get the clicked tab name
        //     var tabName = $(this).attr('data-fieldname');
		// 	alert("")
            
        //     // Handle tab click event
      
        // });
	
		// var htmlContent = "<div id = 'vitals' >Test </div>";

        // Set the HTML content to a field in the form
        // frm.set_value('vitals', htmlContent);
		// setupdata_table("PID-00265")

	},

	
});

function setup_chart(){

// Sample vital signs data
const vitalSignsData = [
	{ datetime: '8:00:00', temperature: 98.6, heartRate: 80, bloodPressure: '120' },
	{ datetime: '12:00:00', temperature: 70.1, heartRate: 82, bloodPressure: '150' },
	{ datetime: '16:00:00', temperature: 97.9, heartRate: 78, bloodPressure: '160' },
	// Add more data entries as needed
  ];
  
  // Function to generate a random color
  function getRandomColor() {
	const letters = '0123456789ABCDEF';
	let color = '#';
	for (let i = 0; i < 6; i++) {
	  color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
  }
  
  // Extract datetimes and vital signs data
  const datetimes = vitalSignsData.map((data) => new Date(data.datetime));
  const vitalSigns = Object.keys(vitalSignsData[0]).filter((key) => key !== 'datetime');
  
  // Create datasets for each vital sign
  const datasets = vitalSigns.map((sign) => ({
	label: sign,
	data: vitalSignsData.map((data) => data[sign]),
	borderColor: getRandomColor(),
	fill: false,
  }));
  
  // Create a new Chart instance
  const ctx = document.getElementById('vitalSignsChart').getContext('2d');
  const chart = new Chart(ctx, {
	type: 'line',
	data: {
	  labels: datetimes,
	  datasets: datasets,
	},
	options: {
	  responsive: true,
	  scales: {
		x: {
		  type: 'time',
		  time: {
			tooltipFormat: 'YYYY-MM-DD HH:mm:ss',
			unit: 'minute',
			displayFormats: {
			  minute: 'YYYY-MM-DD HH:mm',
			},
		  },
		  title: {
			display: true,
			text: 'Date and Time',
		  },
		},
	  },
	},
  });
  
  
  
  
}


function getRandomColor() {
	const letters = '0123456789ABCDEF';
	let color = '#';
	for (let i = 0; i < 6; i++) {
	  color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
  }

function get_history(tab) {
	if (tab == "volunteer"){
		frappe.call({
			method: "rasiin_hr.api.employee_dashbord.volunteer_d", //dotted path to server method
			
			callback: function(r) {
				let data = r.message
			   let columns = [
					
					
				{title:"NO", field:"no"},
				{title:"Full Name", field:"employee_name" ,  headerFilter:"input",},
				{title:"Sex", field:"gender" ,  headerFilter:"input",},
				{title:"Mobile", field:"cell_number" ,  headerFilter:"input",},
				{title:"Department", field:"department" ,  headerFilter:"input",},
				{title:"Designation", field:"designation" ,  headerFilter:"input",},
				{title:"Status", field:"status" ,  headerFilter:"input",},
				{title:"Salary", field:"amount" ,  headerFilter:"input",}

					
				
					
				 ]
				 setup_datatable(columns , data , false , "volunteer")
			 
				
			}})
	}
	if (tab == "employee"){
		frappe.call({
			method: "rasiin_hr.api.employee_dashbord.employee_d", //dotted path to server method
			
			callback: function(r) {
				let data = r.message
			   let columns = [
					
					
					{title:"NO", field:"no"},
					{title:"Full Name", field:"employee_name" ,  headerFilter:"input",},
					{title:"Sex", field:"gender" ,  headerFilter:"input",},
					{title:"Mobile", field:"cell_number" ,  headerFilter:"input",},
					{title:"Department", field:"department" ,  headerFilter:"input",},
					{title:"Designation", field:"designation" ,  headerFilter:"input",},
					{title:"Status", field:"status" ,  headerFilter:"input",},
					{title:"Salary", field:"amount" ,  headerFilter:"input",}

					
				
					
				 ]
				 setup_datatable(columns , data , false , "employee")
			 
				
			}})
	}
	
	
	// let tbldata = []
	// let lab_data = []
	
	// frappe.call({
    //     method: "rasiin_hr.api.employee_dashbord.get_e_dash", //dotted path to server method
        
    //     callback: function(r) {
    //        let columns =  r.message[0][tab]
	// 	   let data = r.message[1][tab]
		 
	// 		console.log(columns)

			
	// 		if(columns){
			
	// 			setup_datatable(columns , data , false , tab)
	// 		}
	// 		else{
				
	// 			setup_datatable([] , [] , false , tab)

			
	// 	}
    //     }})



// 	frappe.call({
// 		method: "his.api.vitals.get_vital", //dotted path to server method
// 		args :{ "patient": patient
// 			},
// 		callback: function(r) {
			
// 			tbldata = r.message
	
   

			
		
		//  let me = this
		// //  let fields = frappe.get_meta("Sales Order").fields
		// 	let columns = [
		// 	// {title:"ID", field:"name"},
		// 	// {title:"Patient", field:"customer"},
		// 	{title:"Date / Time", field:"modified"},
		// 	{title:"Temperature", field:"temperature"},
		// 	{title:"Pulse", field:"pulse"},
		// 	{title:"BP", field:"bp"},
		// 	{title:"Respiration", field:"respiratory_rate"},
		// 	{title:"SpO2", field:"spo"},
		// 	{title:"Height", field:"height"},
		// 	{title:"Weight", field:"weight"},
		// 	{title:"BMI", field:"bmi"},
		// 	{title:"Nurse", field:"owner"},
			
		// 	// {title:"Action", field:"action", hozAlign:"center" , formatter:"html"},
			
		//  ]
	


//
// this.table = new Tabulator("#vitals", {
// 			// layout:"fitDataFill",
// 			layout:"fitDataStretch",
// 			//  layout:"fitColumns",
// 			// responsiveLayout:"collapse",
// 			 rowHeight:30, 
// 			//  selectable:true,
// 			//  dataTree:true,
// 			//  dataTreeStartExpanded:true,
// 			 groupStartOpen:false,
// 			 printAsHtml:true,
// 			//  printHeader:`<img src = '/private/files/WhatsApp Image 2022-10-20 at 6.19.02 PM.jpeg'>`,
// 			//  printFooter:"<h2>Example Table Footer<h2>",
// 			 // groupBy:"customer",
// 			 groupHeader:function(value, count, data, group){
// 				 //value - the value all members of this group share
// 				 //count - the number of rows in this group
// 				 //data - an array of all the row data objects in this group
// 				 //group - the group component for the group
// 			
// 				 return value + "<span style=' margin-left:0px;'>(" + count + "   )</span>";
// 			 },
// 			 groupToggleElement:"header",
// 			//  groupBy:groupbyD.length >0 ? groupbyD : "",
// 			 textDirection: frappe.utils.is_rtl() ? "rtl" : "ltr",
	 
// 			 columns: columns,
			 
		
			 
// 			 data: new_data
// 		 });
		 

// 		}
	
// });
}

function setup_datatable(columns , data , group , tabid){
	// alert(tab)
	// console.log(data)

	// alert(tabid)
	let groupBy = []
	if(group){
		groupBy.push(group)
	}

	let tbl = new Tabulator(`#${tabid}`, {
		// layout:"fitColumns",
		layout:"fitDataFill",
		// layout:"fitDataFill",
		//  layout:"fitColumns",
		// responsiveLayout:"collapse",
		//  rowHeight:30, 
		 placeholder:"No Data Available",
		//  selectable:true,
		//  dataTree:true,
		//  dataTreeStartExpanded:true,
		height:"780px",
		 groupStartOpen:false,
		 printAsHtml:true,
		//  printHeader:`<img src = '/private/files/WhatsApp Image 2022-10-20 at 6.19.02 PM.jpeg'>`,
		 printFooter:"<h2>Example Table Footer<h2>",
		 groupBy:groupBy,
		 groupHeader:function(value, count, data, group){
			 //value - the value all members of this group share
			 //count - the number of rows in this group
			 //data - an array of all the row data objects in this group
			 //group - the group component for the group
		
			 return value + "<span style=' margin-left:0px;'>(" + count + "   )</span>";
		 },
		 groupToggleElement:"header",
		//  groupBy:groupbyD.length >0 ? groupbyD : "",
		//  textDirection: frappe.utils.is_rtl() ? "rtl" : "ltr",
 
		 columns: columns,
		 
		 // [
		 // 	{formatter:"rowSelection", titleFormatter:"rowSelection", hozAlign:"center", headerSort:false, cellClick:function(e, cell){
		 // 		cell.getRow().toggleSelect();
		 // 	  }},
		 // 	{
		 // 		title:"Name", field:"name", width:200,
		 // 	},
		 // 	{title:"Group", field:"item_group", width:200},
		 // ],
		 // [
		 // {title:"Name", field:"name" , formatter:"link" , formatterParams:{
		 // 	labelField:"name",
		 // 	urlPrefix:`/app/${doct}/`,
			 
		 // }},
		 // {title:"Customer", field:"customer" },
		 // {title:"Total", field:"net_total" , bottomCalc:"sum",},
	 
		 // ],
		 
		 data: data
	 });
	 let row = this
	 tbl.on("rowClick", function(e ,rows){
		let target = e.target.nodeName
		//  let selectedRows = row.table.getSelectedRows(); 
		 // console.log(rows._row.data)
		//  console.log(row.table.getSelectedData())
		//  row.toggle_actions_menu_button(row.table.getSelectedData().length > 0);
		if(target != "BUTTON" && target != "I"){
		 frappe.set_route("Form" , "Employee" , rows._row.data.name)
		}
		 // document.getElementById("select-stats").innerHTML = data.length;
	   });
}
