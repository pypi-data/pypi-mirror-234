import spwf

key = "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"
body = input("Email body text: ")
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Set SendGrid API key
sg = SendGridAPIClient(api_key=key)

message = Mail(
    from_email=spwf.output,
    to_emails=spwf.output,
    subject=f'Email from Participant {spwf.participant_number}',
    html_content=f'<strong>{body}</strong>')


try:
    response = sg.send(message)
except Exception as e:
    print(e)
