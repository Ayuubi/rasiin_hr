from frappe.utils.pdf import get_pdf
from frappe.utils import get_site_path, get_formatted_email, get_url
from frappe.utils.file_manager import download_file
import frappe
@frappe.whitelist()
def   generate_pdf():
    html = "<html><body><h1>Hello World!</h1></body></html>"

    pdf_content = get_pdf(html)
    file_doc = frappe.get_doc({
    'doctype': 'File',
    'file_name': 'MyPDF3.pdf',
   
    
    'file_url': '',
    'file_size': len(pdf_content),
    'content': pdf_content
})
    file_doc.save()
    frappe.db.commit()
    

   
    return file_doc.file_url

