import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
key = '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'

def sendMail(receiver,content):
    message = Mail(
        from_email='derickprince.19cs@kct.ac.in',
        to_emails=receiver,
        subject='New job alert!!!!!',
        html_content=content)
    try:
        sg = SendGridAPIClient(key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)