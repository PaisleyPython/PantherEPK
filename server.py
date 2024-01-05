from flask import Flask, render_template, redirect, url_for, request
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
import smtplib
from datetime import datetime
from weasyprint import HTML
import io
import os
import pdfkit
from ironpdf import PdfDocument


app = Flask(__name__)
EMAIL = "discopantherr@gmail.com"
PASSWORD = "drzf kvcn dorb odbw"
TODAY = datetime.today().strftime("%d %B")
config = pdfkit.configuration(
    wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")


# BACK END =========================================

# CONTACT ==========================================


class ContactFormPage(MethodView):

    def get(self):
        contact_form = ContactForm()
        return render_template("contact.html", contactform=contact_form)


class ContactForm(Form):
    # pass

    name = StringField("Name: ", render_kw={"placeholder": "Name"})
    email = StringField("Email: ", render_kw={"placeholder": "Email"})
    message = StringField("Message: ", render_kw={
                          "placeholder": "Message"}, id="message")
    button = SubmitField("Submit")


class SendMail(MethodView):

    def post(self):
        user_input = ContactForm(request.form)
        print(user_input)
        name = str(user_input.data["name"])
        email = str(user_input.data["email"])
        message = str(user_input.data["message"])

        # with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        #     connection.starttls()
        #     connection.login(user=EMAIL, password=PASSWORD)
        #     connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL,
        #                         msg=f"subject:INQUIRY from {name} \n\nFrom: {email}\nMessage: {message}")

        print(f"{name}\n{email}\n{message}")
        return render_template("sent.html")


# INVOICE =================================================


class InvoiceFormPage(MethodView):

    def get(self):
        invoice_form = InvoiceForm()
        return render_template("invoice.html", invoiceform=invoice_form)


class InvoiceForm(Form):

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

    def post(self):
        user_input = InvoiceForm(request.form)
        # today = datetime.today().strftime("%d %B")

        performance = str(user_input.data["performance"])
        company_name = str(user_input.data["company_name"])
        email = str(user_input.data["email"])
        address = str(user_input.data["address"])
        invoice_id = int(user_input.data["invoice_id"])
        amount = int(user_input.data["amount"])
        tax = int(user_input.data["tax"])

        print(f"{TODAY}\n{performance}\n{company_name}\n{
              email}\n{address}\n{invoice_id}\n{amount}\n{tax}\n")

        # render info to HTML and create PDF
        rendered = render_template("invoice_test.html", id=invoice_id, date=TODAY, add=address,
                                   company=company_name, email=email, perf=performance, fee=amount, tax=tax)
        html = HTML(string=rendered)
        html.write_pdf(f'./pdf/invoice.pdf')

        # Turn PDF into JPG to render to send_pdf.html
        pdf = PdfDocument.FromFile("./pdf/invoice.pdf")
        pdf.RasterizeToImageFiles("static/images/invoice.png", DPI=96)

        return render_template("send_pdf.html")
        # return send_file(
        #     f'./pdf/invoice-{TODAY}.pdf')

# html = HTML('templates/invoice_design.html')
# html.write_pdf(f'invoice-{TODAY}.pdf')


# class Password:

#     def password(self):
#         return render_template("password.html")
# ====================================================


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/spec.html")
def spec():
    return render_template("spec.html")


@app.route("/tour.html")
def tour():
    return render_template("tour.html")


@app.route("/images.html")
def images():
    return render_template("images.html")


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('invoice'))
    return render_template('login.html', error=error)


app.add_url_rule('/contact', view_func=ContactFormPage.as_view("contact"))

app.add_url_rule('/sent', view_func=SendMail.as_view("sent"))

app.add_url_rule('/invoice', view_func=InvoiceFormPage.as_view("invoice"))

app.add_url_rule('/invoice_test',
                 view_func=GenerateInvoice.as_view("invoice_test"))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
