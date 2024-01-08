from flask import render_template, request
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from datetime import datetime
from weasyprint import HTML
from ironpdf import PdfDocument
import config

TODAY = datetime.today().strftime("%d %B")

# TODO lowercase form input
# TODO hide environment variables

# INVOICE FORM CREATION ===========================================


class InvoiceFormPage(MethodView):
    """Allows class data to be used on invoice_form.html"""

    def get(self):
        invoice_form = InvoiceForm()
        return render_template("invoice_form.html", invoiceform=invoice_form)


class InvoiceForm(Form):
    """Provides HTML with desired input fields and button"""

    performance = StringField("Performance: ", render_kw={
                              "placeholder": "Performance Type"})
    email = StringField("Email: ", render_kw={"placeholder": "Company Email"})
    company_name = StringField("Company Name: ", render_kw={
                               "placeholder": "Company Name"})
    amount = StringField("Amount: ", render_kw={"placeholder": "Amount"})
    invoice_id = StringField("Invoice ID: ", render_kw={
                             "placeholder": "Invoice ID"})
    add1 = StringField("Add1: ", render_kw={
        "placeholder": "Address line 1 + 2"})
    postcode = StringField("Postcode: ", render_kw={
        "placeholder": "Postcode"})
    city = StringField("City: ", render_kw={
        "placeholder": "City"})

    button = SubmitField("Create PDF")

    """Additional Fields omitted"""
    # add2 = StringField("Add2: ", render_kw={
    #     "placeholder": "Address line 2"})
    # tax = StringField("Tax: ", render_kw={"placeholder": "Tax"})


class GenerateInvoice(MethodView):
    """Takes user input data and writes to PDF"""

    def post(self):

        user_input = InvoiceForm(request.form)

        performance = str(user_input.data["performance"])
        company_name = str(user_input.data["company_name"]).title()
        config.client_email = str(user_input.data["email"]).lower()
        amount = str(user_input.data["amount"])
        invoice_id = str(user_input.data["invoice_id"])
        add1 = str(user_input.data["add1"]).title()
        city = str(user_input.data["city"]).title()
        postcode = str(user_input.data["postcode"]).upper()

        """Additional fields omitted"""
        # tax = int(user_input.data["tax"])

        rendered = render_template("invoice_design.html", date=TODAY, add1=add1, id=invoice_id,
                                   postcode=postcode, city=city, company=company_name, email=config.client_email, perf=performance, fee=amount)
        html = HTML(string=rendered)
        html.write_pdf(f'./pdf/invoice.pdf')

        # Turn PDF into JPG to render to send_pdf.html
        pdf = PdfDocument.FromFile(f"./pdf/invoice.pdf")
        pdf.RasterizeToImageFiles(
            f"static/images/invoice.png", DPI=96)

        return render_template("send_pdf.html")
