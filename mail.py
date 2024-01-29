from flask import render_template
import smtplib
from email.message import EmailMessage
import config
import os

# SENDS INVOICE PDF TO CLIENT =====================================================


class SendEmail():
    """# Creates connection with gmail, populates email fields and send email."""

    def send_email(self):

        DP_EMAIL = os.getenv("PANTHER_EMAIL")
        PASSWORD = os.getenv("EMAIL_API")
        JOHN = "heaton.john@gmail.com"

        msg = EmailMessage()
        msg['Subject'] = 'Amended Perfomance Invoice'
        msg['From'] = DP_EMAIL
        msg['To'] = config.client_email, DP_EMAIL, JOHN
        msg.set_content(
            'Hey there,\n\nPlease see the amended invoice from our recent performance\n\nAll the best\n\nDisco Panther 🐾')

        file = "pdf/invoice.pdf"
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name
            msg.add_attachment(file_data, maintype='application',
                               subtype='octet-stream', filename=file_name)
        with smtplib.SMTP_SSL('smtp.gmail.com', port=465) as smtp:
            smtp.login(DP_EMAIL, PASSWORD)
            smtp.send_message(msg)

        return render_template("sent_pdf.html")


# ============================================================
