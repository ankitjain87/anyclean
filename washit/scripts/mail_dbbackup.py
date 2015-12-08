from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP, SMTP_SSL

import time

DATETIME = time.strftime('%d-%m-%Y')

attachment = '/home/ubuntu/project/anyclean/washit/dbbackup/anyclean' + DATETIME + '.sql'
filename = 'anyclean' + DATETIME + '.sql'

msg = MIMEMultipart()
msg['Subject'] = "DB Backup for " + DATETIME
msg['From'] = ''
msg['To'] = ''

msg.preamble = 'Multipart message.\n'

part = MIMEText("DB backup file.")
msg.attach(part)

try:
    print attachment
    part = MIMEApplication(open(attachment, "rb").read())
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(part)

    mailer = SMTP('smtp.gmail.com', '587')
    mailer.ehlo()
    mailer.starttls()
    mailer.login(‘$username’, ‘$password’)
    mailer.set_debuglevel(1)
    mailer.sendmail(msg['From'], msg['To'].split(', '), msg.as_string())
    mailer.close()
    print "Mail sent with attachment."
except Exception as ex:
    print ex
    print "error............."
