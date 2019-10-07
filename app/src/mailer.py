import logging
import os
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:
    SENDER_ADDRESS = os.getenv('SENDER_ADDRESS')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = int(os.getenv('SMTP_PORT'))

    def __init__(self, generator):
        self.generator = generator
        self.target_address = generator.customer.email

    def send_invoice(self):
        session = self.smtp_session()
        message = self.prepare_message()
        logging.info(f'Sending invoice {self.generator.invoice.number} to {self.target_address}')
        session.sendmail(
            self.SENDER_ADDRESS,
            self.target_address,
            message.as_string()
        )
        session.quit()

    def smtp_session(self):
        session = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        session.starttls(context=ssl.create_default_context())
        session.login(self.SENDER_ADDRESS, self.SENDER_PASSWORD)
        return session

    def prepare_message(self):
        message = MIMEMultipart()
        message['From'] = self.SENDER_ADDRESS
        message['To'] = self.target_address
        message['Subject'] = f'Invoice {self.generator.invoice.number}'
        message.attach(MIMEText(self.message_body(), 'plain'))
        message.attach(self.prepare_payload())
        return message
    
    def message_body(self):
        return '\n'.join([
            f'Attached is invoice {self.generator.invoice.number}.',
            'Feel free to email me if you have any questions.',
            '',
            'Thanks',
            'Sean'
        ])

    def prepare_payload(self):
        payload = MIMEBase('application', 'octate-stream')
        report = self.generator.write_report()
        payload.set_payload(report[1].read())
        encoders.encode_base64(payload)
        payload.add_header(
            'Content-Disposition',
            f'attachment; filename={report[0]}',
        )
        return payload
