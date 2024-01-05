from flask import Flask, render_template, request
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
import smtplib
from datetime import datetime
from weasyprint import HTML
import io
import os

app = Flask(__name__)

# QUOTE ===========================================================


class ContactFormPage(MethodView):

    def get(self):
        contact_form = ContactForm()
        return render_template("contact.html", contactform=contact_form)


class ContactForm(Form):
    pass

    # name = StringField("Name: ", render_kw={"placeholder": "Name"})
    # email = StringField("Email: ", render_kw={"placeholder": "Email"})
    # message = StringField("Message: ", render_kw={
    #                       "placeholder": "Message"}, id="message")
    button = SubmitField("Submit")


class SendMail(MethodView):

    def post(self):
        # user_input = ContactForm(request.form)
        # name = str(user_input.data["name"])
        # email = str(user_input.data["email"])
        # message = str(user_input.data["message"])

        # with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        #     connection.starttls()
        #     connection.login(user=EMAIL, password=PASSWORD)
        #     connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL,
        #                         msg=f"subject:INQUIRY from {name} \n\nFrom: {email}\nMessage: {message}")

        # print(f"{name}\n{email}\n{message}")
        return render_template("sent.html")
        # return render_template("sent.html")

# html = HTML('templates/invoice_test.html')
# html.write_pdf('invoice.pdf')


app.add_url_rule('/contact', view_func=ContactFormPage.as_view("contact"))

app.add_url_rule('/sent', view_func=SendMail.as_view("sent"))


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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
