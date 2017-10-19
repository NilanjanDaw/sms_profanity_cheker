# -*- coding: utf-8 -*-

"""
Send SMS using twilio api
Gets the a/c credentials from credentials.py
"""

# %%
from twilio.rest import Client
from credentials import account_sid, auth_token, my_twilio_no


# %%
def send_msg(msg, phone):
    """ Sends the SMS using Twilio Clent """
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=phone,
        from_=my_twilio_no,
        body=msg)
    print("Message ID:", message.sid)


# %%
