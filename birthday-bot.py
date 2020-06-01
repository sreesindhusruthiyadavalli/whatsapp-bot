import datetime
import requests
import pandas as pd
import re
from twilio.rest import Client
import time

# get birthday list
res = {"items": [{"Name": "sam", "phone":"xxx", "birthday":"19/06/xxx"},
        {"Name": "sam", "phone":"xxx", "birthday":"19/07/xxx"},
        {"Name": "sam", "phone":"xxx", "birthday":"19/05/xxx"}]

}
# unpack
items = res['items']
rows = []
for item in items:
    name = item["Name"] 
    birthday = item["phone"]
    phone = item["birthday"]
    row = [name, birthday, phone]
    rows.append(row)

df = pd.DataFrame(rows)
df.columns = ['Name', 'phone', 'birthday']
df = df.sort_values('Name')

# clean birthdays
df['birthday'] = pd.to_datetime(df['birthday'].astype(str), errors='coerce')
print(df)
dateformat = "%m-%d"
df['birthday'] = df['birthday'].dt.strftime("%m-%d")

# clean phone numbers
def remove_chars(s):
    return re.sub('[^0-9]+', '', s)
df['phone'] = '+91' + df['phone'].apply(remove_chars)

# determine current date
today = datetime.datetime.now()
today = today.strftime("%m-%d")

# filter
birthdays = df[df.birthday == today]

# create client
account_sid = ''
auth_token = 'authtoken'
client = Client(account_sid, auth_token)

# define function
def sendMessage(recipient_number):
    message = client.messages.create(
        body = "Happy Birthday! Have a wonderful day",
        from_ = 'whatsapp:' + recipient_number,
        to = 'whatsapp:' + recipient_number
        #+recipient_number
        )
    print(message.api_version, message.body, message.from_, message.to, message.error_message,message.status)

# send messages
for i in range(0, len(birthdays)):
    recipient_number = birthdays.iloc[i, 1]
    sendMessage(recipient_number)
    print(recipient_number)
    time.sleep(5)


 #References:
#https://www.twilio.com/blog/build-a-whatsapp-chatbot-with-python-flask-and-twilio
#https://www.twilio.com/console
#https://www.youtube.com/watch?v=98OewpG8-yw     
