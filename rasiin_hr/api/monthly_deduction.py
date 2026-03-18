import frappe
import datetime
from datetime import datetime
@frappe.whitelist()
def get_months_ded(rang = None , amount = 0) :
    amount = float(amount)
    months_name = ['Jan' , 'Feb'  , 'Mar' , 'Apr' , 'May' , 'June' , 'July' , 'Agus' , 'Sep' , 'Oct' , 'Nov' , 'Dec']
    months = []
    month = datetime.now().month
    month_name = ""
    month_amount = float(amount) / int(rang)
    deducted_amount = 0
    if rang:
        for i in range(int(rang)):
            month = month
            if month > 12:
                current_month = month-12
                month_name = months_name[current_month-1]
            else:
                month_name = months_name[month-1]
            # months.append(i)
            month = month + 1
            deducted_amount += month_amount
            advance_mon = {
                "month" :month_name,
                "amount" : month_amount,
                "balance" : amount - deducted_amount
            }
            months.append(advance_mon)


    return months
    # for i in range(rang):
