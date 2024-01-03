from flask import Flask, render_template, request
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
import smtplib

app = Flask(__name__)
EMAIL = "discopantherr@gmail.com"
PASSWORD = "drzf kvcn dorb odbw"

# BACK END =========================================

# CONTACT ==========================================


class ContactFormPage(MethodView):

    def get(self):
        contact_form = ContactForm()
        return render_template("contact.html", contactform=contact_form)


class ContactForm(Form):

    name = StringField("Name: ", render_kw={"placeholder": "Name"})
    email = StringField("Email: ", render_kw={"placeholder": "Email"})
    message = StringField("Message: ", render_kw={
                          "placeholder": "Message"}, id="message")
    button = SubmitField("Submit")


class SendMail(MethodView):

    def post(self):
        user_input = ContactForm(request.form)
        name = str(user_input.data["name"])
        email = str(user_input.data["email"])
        message = str(user_input.data["message"])
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL,
                                msg=f"subject:INQUIRY from {name} \n\nFrom: {email}\nMessage: {message}")

        print(f"{name}\n{email}\n{message}")
        return render_template("sent.html")

# QUOTE ===========================================================


class QuoteFormPage(MethodView):

    def get(self):
        quote_form = QuoteForm()
        return render_template("quote.html", quoteform=quote_form)


class QuoteForm(Form):

    performance = StringField("Performance: ", render_kw={
                              "placeholder": "Performance"})
    performance_date = StringField("Performance date: ", render_kw={
                                   "placeholder": "Performance Date"})
    company_name = StringField("Company Name: ", render_kw={
                               "placeholder": "Company Name"})
    email = StringField("Email: ", render_kw={"placeholder": "Company Email"})
    address = StringField("Address: ", render_kw={
                          "placeholder": "Full Address"})
    quote_id = StringField("Quote ID: ", render_kw={"placeholder": "Quote ID"})
    amount = StringField("Amount: ", render_kw={"placeholder": "Amount"})
    tax = StringField("Tax: ", render_kw={"placeholder": "Tax"})

    button = SubmitField("Create PDF")


class GenerateQuote(MethodView):

    def post(self):
        user_input = QuoteForm(request.form)

        performance = str(user_input.data["Performace"])
        performance_date = int(user_input.data("Performance date"))
        company_name = str(user_input.data["Company Name"])
        email = str(user_input.data["Email"])
        address = str(user_input.data["Address"])
        qute_id = int(user_input.data["Quote ID"])
        amount = int(user_input.data["Amount"])
        tax = int(user_input.data["Tax"])

        # print(f"{name}\n{email}\n{message}")
        return render_template("quote.html")


class QuoteToPDF:
    pass


# @app.route("/contact.html")
# def contact():
#     return render_template("contact.html")
app.add_url_rule('/contact', view_func=ContactFormPage.as_view("contact"))

app.add_url_rule('/sent', view_func=SendMail.as_view("sent"))

app.add_url_rule('/quote', view_func=QuoteFormPage.as_view("quote"))


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


if __name__ == "__main__":
    app.run(debug=True)
