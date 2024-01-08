from flask import render_template, request, url_for
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from datetime import datetime
from weasyprint import HTML
from ironpdf import PdfDocument
import pandas as pd
import smtplib
from email.message import EmailMessage

TODAY = datetime.today().strftime("%d %B")
# EMAIL = "discopantherr@gmail.com"
# PASSWORD = "drzf kvcn dorb odbw"

# TODO consider logic for invoice number automation
# TODO lowercase form input

# INVOICE FORM =================


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

    # def __init__(self):
    #     self.client = "discopantherr@gmail.com"
    #     self.invoice_id = 0

    def post(self):

        # TODO i shouldnt need to change anything in here to access the client var?

        user_input = InvoiceForm(request.form)

        # Gather information from HTML input fields
        performance = str(user_input.data["performance"])
        company_name = str(user_input.data["company_name"]).title()
        client = str(user_input.data["email"]).lower()
        amount = int(user_input.data["amount"])
        invoice_id = int(user_input.data["invoice_id"])
        add1 = str(user_input.data["add1"]).title()
        city = str(user_input.data["city"]).title()
        postcode = str(user_input.data["postcode"]).upper()

        """Additional fields omitted"""
        # tax = int(user_input.data["tax"])

        rendered = render_template("invoice_design.html", date=TODAY, add1=add1, id=invoice_id,
                                   postcode=postcode, city=city, company=company_name, email=client, perf=performance, fee=amount)
        html = HTML(string=rendered)
        html.write_pdf(f'./pdf/invoice.pdf')

        # Turn PDF into JPG to render to send_pdf.html
        pdf = PdfDocument.FromFile(f"./pdf/invoice.pdf")
        pdf.RasterizeToImageFiles(
            f"static/images/invoice.png", DPI=96)

        # Creates connection with gmail, populates email fields and send email.

        return render_template("send_pdf.html")


class SendEmail(GenerateInvoice):

    def send_email(self):

        EMAIL = "discopantherr@gmail.com"
        PASSWORD = "drzf kvcn dorb odbw"

        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL,
                                msg=f"subject:TEST TEST \n\nFrom: {EMAIL}\nMessage: TEST TEST")

        msg = EmailMessage()
        msg['Subject'] = 'Perfomance Invoice'
        msg['From'] = EMAIL
        msg['To'] = ""
        msg.set_content(
            'Hey there,\n\nPlease see the attached invoice from our recent performance\n\nAll the best\n\nDisco Panther 🐾')

        file = "pdf/invoice.pdf"
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name
            msg.add_attachment(file_data, maintype='application',
                               subtype='octet-stream', filename=file_name)
        with smtplib.SMTP_SSL('smtp.gmail.com', port=465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        return render_template("sent_pdf.html")
