from anyclean import models

import config
import plivo


auth_id = "SOMEAUTH"
auth_token = "SOMETOKEN"

p = plivo.RestAPI(auth_id, auth_token)


def send_text(dst_number, text):
    if config.DEV_ENV:
        print "To: " + dst_number, text
        return True
        
    dst_number = '+91' + dst_number

    params = {
        'src': '1202XXXXXX', # Caller Id
        'dst' : dst_number, # User Number to Call
        'text' : text,
        'type' : 'sms',
        'url' : "http://localhost/smsReport", # The URL to which with the status of the message is sent
        'method' : 'POST' # The method used to call the url
    }

    return p.send_message(params)
