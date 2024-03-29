from flask import Flask, render_template, redirect, url_for, request
import os
from contact import SendMail, ContactFormPage
from invoice import InvoiceFormPage, GenerateInvoice
from mail import SendEmail

# TODO Anything addtional needed for requirements.txt to deploy?

app = Flask(__name__)

# 'Contact us' page imports =============================

app.add_url_rule('/sent', view_func=SendMail.as_view("sent"))
app.add_url_rule('/contact', view_func=ContactFormPage.as_view("contact"))

# Invoice generator imports =============================

app.add_url_rule('/invoice', view_func=InvoiceFormPage.as_view("invoice"))
app.add_url_rule(
    '/invoice_design', view_func=GenerateInvoice.as_view("invoice_design"))

# sent pdf imports ======================================


@app.route("/send_pdf", methods=['POST'])
def send_pdf():
    SendEmail().send_email()
    return render_template('sent_pdf.html')

# Login page logic ======================================


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('invoice'))
    return render_template('login.html', error=error)

# Web page routes ======================================


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

# ================================================


if __name__ == '__main__':
    # app.run()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
