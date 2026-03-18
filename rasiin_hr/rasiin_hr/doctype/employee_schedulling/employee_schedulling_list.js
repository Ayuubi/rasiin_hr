frappe.listview_settings["Employee Schedulling"] = {
  onload(listview) {
    listview.page.add_inner_button(__("Import Schedule (Excel)"), () => {
      const d = new frappe.ui.Dialog({
        title: __("Import Employee Schedule"),
        fields: [
          {
            fieldtype: "Attach",
            fieldname: "file",
            label: __("Excel File"),
            reqd: 1,
          },
          {
            fieldtype: "Int",
            fieldname: "year",
            label: __("Year"),
            default: new Date().getFullYear(),
            reqd: 1,
          },
          {
            fieldtype: "Select",
            fieldname: "month",
            label: __("Month"),
            reqd: 1,
            options: [
              { label: "January", value: 1 },
              { label: "February", value: 2 },
              { label: "March", value: 3 },
              { label: "April", value: 4 },
              { label: "May", value: 5 },
              { label: "June", value: 6 },
              { label: "July", value: 7 },
              { label: "August", value: 8 },
              { label: "September", value: 9 },
              { label: "October", value: 10 },
              { label: "November", value: 11 },
              { label: "December", value: 12 },
            ],
            default: new Date().getMonth() + 1,
          },
          {
            fieldtype: "Check",
            fieldname: "overwrite",
            label: __("Overwrite existing (same employee + date)"),
            default: 0,
          },
        ],
        primary_action_label: __("Import"),
        primary_action: async (values) => {
          if (!values.file) return;

          d.hide();
          frappe.show_alert({ message: __("Import started..."), indicator: "blue" });

          const r = await frappe.call({
            method: "rasiin_hr.setup.data_importer.import_employee_schedule_from_file",
            args: {
              file_url: values.file,
              year: values.year,
              month: values.month,
              overwrite: values.overwrite ? 1 : 0,
            },
            freeze: true,
            freeze_message: __("Importing schedule..."),
          });

          const res = r.message || {};
          frappe.msgprint({
            title: __("Import Result"),
            indicator: res.errors ? "red" : "green",
            message: `
              <b>Inserted:</b> ${res.inserted || 0}<br>
              <b>Updated:</b> ${res.updated || 0}<br>
              <b>Skipped:</b> ${res.skipped || 0}<br>
              <b>Errors:</b> ${res.errors || 0}<br>
              <b>Month:</b> ${res.month || ""} ${res.year || ""}
            `,
          });

          listview.refresh();
        },
      });

      d.show();
    });
  },
};
