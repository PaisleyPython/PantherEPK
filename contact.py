from flask import Flask, render_template, request
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
import smtplib

EMAIL = "discopantherr@gmail.com"
PASSWORD = "drzf kvcn dorb odbw"


class ContactFormPage(MethodView):

    # def __init__(self, email, password):
    #     self.email = email
    #     self.password = password

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

        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL,
                                msg=f"subject:ENQUIRY from {name} \n\nFrom: {email}\nMessage: {message}")

        print(f"{name}\n{email}\n{message}")
        return render_template("sent.html")
