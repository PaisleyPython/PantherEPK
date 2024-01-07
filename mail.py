import pandas as pd
import smtplib
from email.message import EmailMessage
from flask import render_template, request
from flask.views import MethodView
from wtforms import Form, SubmitField


# TODO do I need a loop to send to myself as well as the client, or is there a method for that?
# TODO Need to be able to extract email from the invoice form...!?

def post():
    # user = SendButton(request.form)
    EMAIL = "discopantherr@gmail.com"
    PASSWORD = "drzf kvcn dorb odbw"

    msg = EmailMessage()
    msg['Subject'] = 'Perfomance Invoice'
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    msg.set_content(
        'Meow, \n Please see attached invoice from our recent performance \n Att, \n Disco Panther 🐾')

    file = './pdf/invoice.pdf'
    with open(file, 'rb') as f:
        file_data = f.read()
        file_name = f.name
        msg.add_attachment(file_data, maintype='application',
                           subtype='octet-stream', filename=file_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)
        print(count)
        count = count+1

        # return render_template("sent_pdf.html")


# <ul class="actions">
        # 	<li><a href="#" class="button">Send to client</a></li>
        # </ul>
