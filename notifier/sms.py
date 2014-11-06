import json
import httplib, urllib
import logging
from domotica import settings

HOST = "rest.nexmo.com"
PATH = "/sms/json"
URL = "https://rest.nexmo.com/sms/json"

def build_request(text, to):
    smsreq = {}
    smsreq['api_key'] = settings.API_KEY
    smsreq['api_secret'] = settings.API_SECRET
    smsreq['from'] = "Domotica Pennestraat"
    smsreq['to'] = to
    smsreq['text'] = text

    return smsreq

def send_request(smsreq):
    params = urllib.urlencode(smsreq)
    headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }
    conn = httplib.HTTPConnection(HOST)
    conn.request("POST", PATH, params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

    return data

def parse_message(m):
    if m['status'] != "0":
        raise Exception("Bad message status %s" % m['status'])
    return m['remaining-balance']

def parse_response(r):
    for m in r['messages']:
        remaining_balance = parse_message(m)
    return remaining_balance

def send(text, to):
    smsreq = build_request(text, to)
    response = send_request(smsreq)

    try:
        data = json.loads(response)
        remaining_balance = parse_response(data)

        if float(remaining_balance) < 2:
            logging.warning("Remaining balance is only %s!" % remaining_balance)
    except Exception, e:
        logging.error("Failed to parse response (%s): %s" % (response, e))
        return False

    return True
