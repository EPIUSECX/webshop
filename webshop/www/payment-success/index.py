import frappe
from frappe import _

no_cache = 1


def get_context(context):
	"""Get context for payment success page"""
	context.no_cache = 1
	context.body_class = "payment-page"
	
	# Get payment details from query parameters
	doctype = frappe.local.form_dict.get("doctype")
	docname = frappe.local.form_dict.get("docname")
	redirect_to = frappe.local.form_dict.get("redirect_to")
	
	context.payment_message = ""
	context.doc = None
	context.error_message = ""
	context.redirect_to = redirect_to or "/"
	context.order_name = None
	
	# Try to get the document (Payment Request, Sales Order, etc.)
	if doctype and docname:
		try:
			doc = frappe.get_doc(doctype, docname)
			context.doc = doc
			context.order_name = doc.reference_name if hasattr(doc, "reference_name") else docname
			
			if hasattr(doc, "get_payment_success_message"):
				context.payment_message = doc.get_payment_success_message()
			else:
				context.payment_message = _("Payment completed successfully!")
		except Exception as e:
			context.error_message = _("Document not found or access denied.")
			context.payment_message = _("Payment completed successfully!")
			frappe.log_error(f"Payment success page error: {str(e)}", "Payment Success Page")
	else:
		# No document specified - generic success message
		context.payment_message = _("Payment completed successfully!")
	
	# Set breadcrumbs
	context.parents = [
		{"name": _("Home"), "route": "/"},
		{"name": _("Payment"), "route": "#"}
	]
	
	# Get order details if available
	if context.order_name:
		try:
			order_doc = frappe.get_doc("Sales Order", context.order_name)
			context.order_total = order_doc.get_formatted("grand_total")
		except:
			pass

