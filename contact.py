from flask import Flask, render_template, request
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
import smtplib

# TODO will have to creae enviro vars to hide this data
# Connection to Gmail
EMAIL = "discopantherr@gmail.com"
PASSWORD = "drzf kvcn dorb odbw"

# CONTACT FORM ===================


class ContactFormPage(MethodView):
    """Allows class data to be used on invoice.html"""

    def get(self):
        contact_form = ContactForm()
        return render_template("contact.html", contactform=contact_form)


class ContactForm(Form):
    """Provides HTML with desired input fields and button"""

    name = StringField("Name: ", render_kw={"placeholder": "Name"})
    email = StringField("Email: ", render_kw={"placeholder": "Email"})
    message = StringField("Message: ", render_kw={
                          "placeholder": "Message"}, id="message")
    button = SubmitField("Submit")


class SendMail(MethodView):
    """Takes user data, populates and sends email to bands email address"""

    def post(self):
        user_input = ContactForm(request.form)

        # Gather information from HTML input fields
        name = str(user_input.data["name"])
        email = str(user_input.data["email"])
        message = str(user_input.data["message"])

        # Creates connection with gmail, populates email fields and send email.
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL,
                                msg=f"subject:ENQUIRY from {name} \n\nFrom: {email}\nMessage: {message}")

        # print(f"{name}\n{email}\n{message}")
        return render_template("sent.html")
