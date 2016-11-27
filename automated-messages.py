from twilio.rest import TwilioRestClient
from twilio import twiml
import datetime

account_sid = "AC0bdf8036e6590c7833e0766423192f3f"
auth_token = "4f9a0e84bbee241ea73ad380f9255925"
n = "6476949837"
client = TwilioRestClient(account_sid, auth_token)

phone_book ={"Fei":"6472333048",
            "Anupya":"6479940655",
            "He Yue":"5195888188",
            "Fizaa":"",
            "Ankita":"5197814838",
            "Shreya":""}

def make_symptoms():
    ws={}
    for i in range (1,280//7+1):
        ws[i]="week " + str(i) + " symptoms"
    return ws

weekly_symptoms = make_symptoms()

def send_sms(number,msg,url):
    if url=="":
        client.messages.create(
            to = number,
            from_ = n,
            body = msg,
            )
    else:
        client.messages.create(
            to = number,
            from_ = n,
            body = msg,
            media_url = url,
            )

def find_week_from_string(d):
    due_day = int(d[0:2])
    due_month = int(d[3:5])
    due_year = int(d[6:])
    
    duedate=datetime.date(due_year,due_month,due_day)
    today = datetime.date.today()
    
    difference = duedate-today
    days_elapsed = 280-difference.days
    week = (days_elapsed//7)+1

    return week

def find_week_info(duedate):
    today = datetime.date.today()
    difference = duedate-today
    days_elapsed = 280-difference.days
    week = (days_elapsed//7)+1
    symptoms = weekly_symptoms[week]
    if week==1:
        url="http://www.pregnancycorner.com/wp-content/uploads/1-week-pregnant.jpg"
    else:
        url="http://www.pregnancycorner.com/wp-content/uploads/"+str(week)+"-weeks-pregnant.jpg"
    return [symptoms,url]

def send_weekly_message(duedate,number):
    week_info = find_week_info(duedate)
    send_sms(number,week_info[0],week_info[1])

def main(due_year,due_month,due_day,number):
    duedate=datetime.date(due_year,due_month,due_day)
    send_weekly_message(duedate,number)

def respond(sentence):
  words = sentence.split()
  if (("baby" in words) and (("move" in words) or ("moving" in words))):
      return "You can start to feel the baby's movement anytime from 16-22 weeks, " + \
            "and the baby may not move very frequently until 24 weeks. " + \
    "Though do contact us if the baby doesn't move everyday after 24 weeks. " \
    + "See more at " + \
    "http://blogs.webmd.com/womens-health/2015/10/babys-movement-during-pregnancy-whats-normal.html"
  if ("exercise" in words):
      return "You should definitely exercise during your pregnancy. " + \
             "At least 20 minutes of exercise with moderate intensity per day " + \
             "is recommend. " + "See more at " + \
             "http://www.babycenter.com/0_the-best-kinds-of-exercise-for-pregnancy_7880.bc"
  if (("nausea" in words) or ("nauseous" in words) or ("vomit" in words) or ("vomiting" in words)):
      return "Nausea and vomiting is common during pregnancy. " + \
             "It will not affect the health of your baby whether you have it or not. " + \
             "Just remember to stay hydrated. " + "See more at " + \
             "http://www.babycenter.com/morning-sickness?page=1"
  return "Sorry, no answer to your question is found, we are trying our best"  + \
         "to complete the database. " + \
         "In the meantime, please text # to talk to a doctor."

def question_response(number,sentence):
      msg=respond(sentence)
      send_sms(number,msg,"")
      
