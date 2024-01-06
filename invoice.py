from flask import render_template, request
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from datetime import datetime
from weasyprint import HTML
from ironpdf import PdfDocument

TODAY = datetime.today().strftime("%d %B")

# INVOICE FORM =================


class InvoiceFormPage(MethodView):
    """Allows class data to be used on invoice.html"""

    def get(self):
        invoice_form = InvoiceForm()
        return render_template("invoice.html", invoiceform=invoice_form)


class InvoiceForm(Form):
    """Provides HTML with desired input fields and button"""

    performance = StringField("Performance: ", render_kw={
                              "placeholder": "Performance"})
    email = StringField("Email: ", render_kw={"placeholder": "Company Email"})
    company_name = StringField("Company Name: ", render_kw={
                               "placeholder": "Company Name"})
    invoice_id = StringField("Invoice ID: ", render_kw={
        "placeholder": "Invoice ID"})
    address = StringField("Address: ", render_kw={
                          "placeholder": "Full Address"})
    amount = StringField("Amount: ", render_kw={"placeholder": "Amount"})
    tax = StringField("Tax: ", render_kw={"placeholder": "Tax"})

    button = SubmitField("Create PDF")


class GenerateInvoice(MethodView):
    """Takes user input data and writes to PDF"""

    def post(self):
        user_input = InvoiceForm(request.form)

        # Gather information from HTML input fields
        performance = str(user_input.data["performance"])
        company_name = str(user_input.data["company_name"])
        email = str(user_input.data["email"])
        address = str(user_input.data["address"])
        invoice_id = int(user_input.data["invoice_id"])
        amount = int(user_input.data["amount"])
        tax = int(user_input.data["tax"])

        rendered = render_template("invoice_test.html", id=invoice_id, date=TODAY, add=address,
                                   company=company_name, email=email, perf=performance, fee=amount, tax=tax)
        html = HTML(string=rendered)
        html.write_pdf(f'./pdf/invoice.pdf')

        # Turn PDF into JPG to render to send_pdf.html
        pdf = PdfDocument.FromFile("./pdf/invoice.pdf")
        pdf.RasterizeToImageFiles("static/images/invoice.png", DPI=96)

        return render_template("send_pdf.html")
