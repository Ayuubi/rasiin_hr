frappe.listview_settings['Employee'] = {
    // 	add_fields: ["status"],
        get_indicator: function(doc) {
            return [__(doc.status), {
                "Active": "blue",
                "Inactive" : "red",
               
            }[doc.status], "status,=," + doc.status];
        },
        // onload: function(listview) {
        //       listview.filter_area.add(filters);
        //        var filters = [["Employee", "volunteer", "=", 0]];
        //         listview.filter_area.add(filters);
        //     listview.page.set_secondary_action(__(`<input type="checkbox" id="demoCheckbox" name="checkbox" value="1"> Volunteer`), function() {
        //         filter_value = listview.filter_area.filter_list.filters['0'].value
        //         var filters = [["Employee", "volunteer", "=", !filter_value]];
            
        //     //   listview.filter_list.clear_filters();
          
        //     console.log(listview.filter_area.filter_list)
        //    listview.filter_area.filter_list.clear_filters()
        //     listview.filter_area.add(filters);
        //     // listview.refresh();
               
        //         // listview.run();
        //     });
        // }
    };
    
    