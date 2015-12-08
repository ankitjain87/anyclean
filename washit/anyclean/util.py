from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP, SMTP_SSL

import config
import constants


def send_mail(receivers, subject, content, attachment=None, filename=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = config.FROM_EMAIL
    msg['To'] = receivers

    if config.DEV_ENV:
        msg['To'] = config.TEST_TO_EMAIL

    msg.preamble = 'Multipart message.\n'

    part = MIMEText(content)
    msg.attach(part)

    if attachment:
        part = MIMEApplication(open(attachment, "rb").read())
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)

    mailer = SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT)
    # mailer.ehlo()
    # mailer.starttls()
    mailer.login(config.USERNAME, config.PASSWORD)
    mailer.set_debuglevel(1)
    mailer.sendmail(msg['From'], msg['To'].split(', '), msg.as_string())
    mailer.close()