import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# private key is protected here

message = Mail(
    from_email='derickprince.19cs@kct.ac.in',
    to_emails=['vishwa19bcs100@gmail.com','baskarderick@gmail.com','madhanvarshini3@gmail.com','sbn12kk@gmail.com'],
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(key)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
