frappe.pages['employee-schedule'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Employee Schedule',
		single_column: true
	});
}

frappe.pages['employee-schedule'].on_page_load = function(wrapper) {
	new EmpSched(wrapper)
}

EmpSched = Class.extend(
	{
		init:function(wrapper){
			this.page = frappe.ui.make_app_page({
				parent : wrapper,
				title: 'Personal Schedulle',
				single_column : true
			});
			// this.tbldata = []
			
			this.make()
			this.create_btns()
		
		
		},
		make:function(){
			let me = this
			$(frappe.render_template(frappe.dashbard_page.body, me)).appendTo(me.page.main)
			setTimeout(() => {
				frappe.db.get_value("Employee" , {"user_id" : frappe.session.user}, "name").then( r =>{
					let cu_e = r.message.name
					create_clander(cu_e)
				})
				
				
			}, 200);
			createYear = generate_year_range(1970, 2050);
/** or
 * createYear = generate_year_range( 1970, currentYear );
 */

			document.getElementById("year").innerHTML = createYear;
		
			





		
		},
		
		create_btns:function(){

		

			let emp = this.page.add_field({
				label: 'Employee',
				fieldtype: 'Link',
				fieldname: 'em',
				options: "Employee",
			
				change() {
				
					let empl = emp.get_value()
					create_clander(empl)
				}
			});
		},


	

	
	
	}

	
)


function generate_year_range(start, end) {
    var years = "";
    for (var year = start; year <= end; year++) {
        years += "<option value='" + year + "'>" + year + "</option>";
    }
    return years;
}



today = new Date();
currentMonth = today.getMonth();
currentYear = today.getFullYear();
selectYear = $("#year");
selectMonth = $("#month");


// createYear = generate_year_range(1970, 2050);
// /** or
//  * createYear = generate_year_range( 1970, currentYear );
//  */

// $("#year").html(createYear);

var calendar = $("#calendar");
// var lang = calendar.getAttribute('data-lang');

var months = "";
var days = "";

var monthDefault = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

var dayDefault = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];


months = monthDefault;
days = dayDefault;
let cur_emp = ''

function create_clander(emp){
	cur_emp = emp
	var $dataHead = "<tr>";
for (dhead in days) {
    $dataHead += "<th data-days='" + days[dhead] + "'>" + days[dhead] + "</th>";
}
$dataHead += "</tr>";


$("#thead-month").html($dataHead);


monthAndYear = $("#monthAndYear");
showCalendar(currentMonth, currentYear , emp);
}




function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCalendar(currentMonth, currentYear , cur_emp);
}

function previous() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    showCalendar(currentMonth, currentYear , cur_emp);
}

function jump() {

    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    showCalendar(currentMonth, currentYear , cur_emp);
}

function showCalendar(month, year , emp) {


    var firstDay = ( new Date( year, month ) ).getDay();

    tbl = $("#calendar-body");

    
    tbl.html("");
	if(emp){
		
	
	frappe.db.get_value("Employee" , emp , 'employee_name')
	.then(r => {
    if(r.message.employee_name){
		// emp_name = frappe.get_doc("Employee" , emp )

			// console.log(emp)
			monthAndYear.html("<span> " + r.message.employee_name + "</span> <br>" + months[month] + " " + year  );
			
	
	

	}
	else {
		monthAndYear.html("<span> " + frappe.session.user_fullname + "</span> <br>" + months[month] + " " + year  );
	}
  
    selectYear.value = year;
    selectMonth.value = month;
	// console.log(months[month])

    // creating all cells
    var date = 1;
	var shift_list = {}
	filters = {
		"user_id" : frappe.session.user
	}
	if(emp){
		filters = {
			"employee" : emp,
		}

	}

	frappe.db.get_list(
		"Employee Schedulling" , {
			filters :{
				"employee" : emp,
				"year" : 2024
			},
			fields :["day" , "shift" , "label" , "month" , "year"],
			limit : 1000
		}
	).then(sch => {
		sch.forEach(el => {
			if(el.month == months[month] && el.year == year){
				// if(el.year == year){
			shift_list[el.day] = el.shift
			// console.log(months[month])
			// console.log(el.month)
			
			}
			// console.log(el.month )
			// console.log(months[month])

			
		});
		
		for ( var i = 0; i < 6; i++ ) {
        
			var row = document.createElement("tr");
	
			
			for ( var j = 0; j < 7; j++ ) {
				if ( i === 0 && j < firstDay ) {
					cell = document.createElement( "td" );
					cellText = document.createTextNode("");
					cell.appendChild(cellText);
					row.appendChild(cell);
				} else if (date > daysInMonth(month, year)) {
					break;
				} else {
	
					cell = document.createElement("td");
					cell.setAttribute("data-date", date);
					cell.setAttribute("data-month", month + 1);
					cell.setAttribute("data-year", year);
					cell.setAttribute("data-month_name", months[month]);
					cell.className = "date-picker";
					
					if(shift_list[date]){
						// cell.innerHTML = `<span class= ${class_}> ${date}  </span> <br> <span > ${shift_list[date]} </span>`;
						class_ = ''
						if(shift_list[date] == "Free"){
							class_ = "night"
							shift_list[date] = "Off"
						}
						else if(shift_list[date] == "Night Shift"){
							// class_ = "night"
							shift_list[date] = "Night"
						}
						else if(shift_list[date] == "Day Shift"){
							// class_ = "night"
							shift_list[date] = "Day"
						}
						// alert(shift_list[date])
						cell.innerHTML = `<span class= ${class_}> ${date}  </span> <br> <span  class= ${class_}> ${shift_list[date]} </span>`;
					}
					else{
						cell.innerHTML = "<span>" + date +"</span>";
					}
					
	
					if ( date === today.getDate() && year === today.getFullYear() && month === today.getMonth() ) {
						cell.className = "date-picker selected";
					}
					row.appendChild(cell);
					date++;
				}
	
	
			}
	
			tbl.append(row);
		}
	
	})
})
}
}

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}


let emp_sc_body = `

<div class="cl_wrapper">
<div class="container-calendar">
	<h3 id="monthAndYear"></h3>
	<div class="button-container-calendar">
		<button id="previous" onclick="previous()">&#8249;</button>
		<button id="next" onclick="next()">&#8250;</button>
	</div>
	<table class="table-calendar" id="calendar" data-lang="en">
		<thead id="thead-month"></thead>
		<tbody id="calendar-body"></tbody>
	</table>
	<div class="footer-container-calendar">
		 <label for="month">Jump To: </label>
		 <select id="month" onchange="jump()">
			 <option value=0>Jan</option>
			 <option value=1>Feb</option>
			 <option value=2>Mar</option>
			 <option value=3>Apr</option>
			 <option value=4>May</option>
			 <option value=5>Jun</option>
			 <option value=6>Jul</option>
			 <option value=7>Aug</option>
			 <option value=8>Sep</option>
			 <option value=9>Oct</option>
			 <option value=10>Nov</option>
			 <option value=11>Dec</option>
		 </select>
		 <select id="year" onchange="jump()"></select>       
	</div>
</div>
</div>

`


frappe.dashbard_page = {
	body : emp_sc_body
}
