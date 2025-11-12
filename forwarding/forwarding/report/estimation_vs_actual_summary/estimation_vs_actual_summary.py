# Copyright (c) 2022, FirstERP and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)

	# columns_for_total = [row['fieldname'] for row in columns if row['fieldtype']=="Currency"]
	# totals = {}

	# for col in columns_for_total:
	# 	totals.setdefault(col,0)
	# totals.setdefault(columns[0]['fieldname'],"Totals")
	# totals.setdefault('bold',1)
	
	# for col in columns_for_total:
	# 	for row in data:
	# 		if isinstance(row,dict):
	# 			if row[col]:
	# 				print(col,":-" ,totals[col])
	# 				totals[col] += float(row[col])
	
	# data.append(totals)
	return columns,data


def get_conditions(filters):
	conditions = ""
	if filters.get('from_date'):
		conditions += " and `tabOperations`.date >= %(from_date)s"# %filters.get('from_date')

	if filters.get('to_date'):
		conditions += " and `tabOperations`.date <= %(to_date)s"# %filters.get('to_date')

	if filters.get('customer'):
		conditions += " and `tabOperations`.customer = %(customer)s"# %filters.get('to_date')

	if filters.get('operations'):
		conditions += " and `tabOperations`.name = %(operations)s"# %filters.get('to_date')

	if filters.get('branch'):
		conditions += " and `tabOperations`.branch = %(branch)s"# %filters.get('to_date')

	return conditions

	
def get_data(filters):
	conditions = get_conditions(filters)
	print(conditions)
	data = frappe.db.sql('''
						SELECT
							`tabOperations`.name as operations,
							`tabOperations`.date as date,
							`tabOperations`.customer as customer,
							`tabOperations`.branch as branch,
							`tabOperations`.operations_status as status,
							SUM( `tabGL Entry`.credit )as actual_income,
							SUM( `tabGL Entry`.debit )as actual_expense,
							( SUM(`tabGL Entry`.credit) -   SUM(`tabGL Entry`.debit) ) as actual_p_n_l, 
							CAST(`tabOperations`.total_rate AS DECIMAL(10,2)) as estimated_income,
							CAST(`tabOperations`.total_cost AS DECIMAL(10,2)) as estimated_expense,
							(`tabOperations`.total_rate - `tabOperations`.total_cost) as estimated_p_n_l
						FROM
							`tabOperations`
						LEFT JOIN 
	 						`tabGL Entry` 
	 					ON 
	 						(`tabGL Entry`.project = `tabOperations`.name
							AND
								`tabGL Entry`.account in (select name from `tabAccount` where account_type in ('Income Account','Cost of Goods Sold') )
							AND `tabGL Entry`.is_cancelled=0 
							 )
						WHERE
							`tabOperations`.docstatus !=2 
							%s
						GROUP BY
							`tabOperations`.name
	''' %conditions,filters,as_dict=1)

	# data = frappe.db.sql('''
	# 				Select 
	# 					`tabOperations`.name as operations,
	# 					`tabOperations`.date as date,
	# 					`tabOperations`.customer as customer,
	# 					`tabOperations`.branch as branch,
	# 					`tabOperations`.operation_status as status,
	# 					SUM( `tabGL Entry`.credit )as actual_income,
	# 					SUM( `tabGL Entry`.debit )as actual_expense,
	# 					( SUM(`tabGL Entry`.credit) -   SUM(`tabGL Entry`.debit) ) as actual_p_n_l, 
	# 					`tabOperations`.total_rate as estimated_income,
	# 					`tabOperations`.total_cost as estimated_expense,
	# 					(`tabOperations`.total_rate - `tabOperations`.total_cost) as estimated_p_n_l
	# 				From
	# 					`tabOperations` 
	# 				LEFT JOIN 
	# 					`tabGL Entry` 
	# 				ON 
	# 					(`tabGL Entry`.project = `tabOperations`.name 
	# 					AND 
	# 						`tabGL Entry`.account in (select name from `tabAccount` where account_type in ('Income Account','Cost of Goods Sold')))
					
	# 				Where 
	# 					`tabOperations`.docstatus !=2 
	# 					%s
	# 				GROUP BY
    # 					`tabOperations`.name		
	# 				''' %conditions,filters,as_dict=1)
	print(data)
	return data
    
def get_columns(filters):
	columns = [
			{
				'label': _('Operations'),
				'fieldname': 'operations',
				'fieldtype': 'Link',
				'options': 'Operations',
				'width': 140
			},
			{
				'label': _('Date'),
				'fieldname': 'date',
				'fieldtype': 'Date',
				'width': 120
			},
			{
				'label': _('Customer'),
				'fieldname': 'customer',
				'fieldtype': 'Link',
				'options': 'Customer',
				'width': 120
			},
			{
				'label': _('Branch'),
				'fieldname': 'branch',
				'fieldtype': 'Link',
				'options': 'Branch',
				'width': 120
			},
			{
				'label': _('Status'),
				'fieldname': 'status',
				'fieldtype': 'Data',
				'width': 120
			},
			{
				'label': _('Actual Income'),
				'fieldname': 'actual_income',
				'fieldtype': 'Currency',
				'width': 90
			},
			{
				'label': _('Actual Expense'),
				'fieldname': 'actual_expense',
				'fieldtype': 'Currency',
				'width': 90
			},
			{
				'label': _('Actual Profit & Loss'),
				'fieldname': 'actual_p_n_l',
				'fieldtype': 'Currency',
				'width': 90
			},
			{
				'label': _('Estimated Income'),
				'fieldname': 'estimated_income',
				'fieldtype': 'Currency',
				'width': 90
			},
			{
				'label': _('Estimated Expense'),
				'fieldname': 'estimated_expense',
				'fieldtype': 'Currency',
				'width': 90
			},
			{
				'label': _('Estimated Profit & Loss'),
				'fieldname': 'estimated_p_n_l',
				'fieldtype': 'Currency',
				'width': 90
			}
		]
	return columns