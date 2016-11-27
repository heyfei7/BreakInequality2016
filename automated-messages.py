from twilio.rest import TwilioRestClient
from twilio import twiml
import datetime

account_sid = "AC0bdf8036e6590c7833e0766423192f3f"
auth_token = "4f9a0e84bbee241ea73ad380f9255925"
n = "6476949837"
client = TwilioRestClient(account_sid, auth_token)

phone_book ={"Fei":"6472333048",
            "Anupya":"6479940655",
            "Hu Yue":"5195888188",
            "Fizaa":"",
            "Ankita":"",
            "Shreya":""}

def make_symptoms():
    ws={}
    for i in range (1,280//7+1):
        ws[i]="week " + str(i) + " symptoms"
    return ws

weekly_symptoms = make_symptoms()

def send_sms(number,msg,url):
    client.messages.create(
        to = number,
        from_ = n,
        body = msg,
        media_url = url,
        )

def find_week(duedate,today):
    difference = duedate-today
    total_days = 280
    days_elapsed = total_days-difference.days
    week = (days_elapsed//7)+1
    symptoms = weekly_symptoms[week]
    if week==1:
        url="http://www.pregnancycorner.com/wp-content/uploads/1-week-pregnant.jpg"
    else:
        url="http://www.pregnancycorner.com/wp-content/uploads/"+str(week)+"-weeks-pregnant.jpg"
    return [symptoms,url]

def send_weekly_message(duedate,number):
    today = datetime.date.today()
    week_info = find_week(duedate,today)
    send_sms(number,week_info[0],week_info[1])

def main(due_year,due_month,due_day,number):
    duedate=datetime.date(due_year,due_month,due_day)
    send_weekly_message(duedate,number)
