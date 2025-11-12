// Copyright (c) 2022, FirstERP and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Estimation Vs Actual Summary"] = {
	"filters": [
		{
			"fieldname":"operations",
			"label": __("Operations"),
			"fieldtype": "Link",
			"options": "Operations"
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
		}

	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		// console.log(data)
		if (data && data.bold) {
			value = value.bold();

		}
		// if(column.colIndex==1){
		// 	console.log(column.fieldname)
		// 	if(data[column.fieldname]=="Totals"){
		// 		// value = value.bold()
		// 		// data = data.bold()
		// 		console.log(value)
		// 	}
		// }
		return value;
	}
};
