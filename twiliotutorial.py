from twilio.rest import TwilioRestClient
# put your own credentials here
ACCOUNT_SID = '<AccountSid>'
AUTH_TOKEN = '<AuthToken>'

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

client.messages.create(
    to = '<ToNumber>',
    from_ = '<FromNumber>',
    body = '<BodyText>',
)
           
# Using Flask
#########################################################################
from reminders import celery, db, app
from models.appointment import Appointment
from sqlalchemy.orm.exc import NoResultFound
from twilio.rest import TwilioRestClient
import arrow

twilio_account_sid = app.flask_app.config['TWILIO_ACCOUNT_SID']
twilio_auth_token = app.flask_app.config['TWILIO_AUTH_TOKEN']
twilio_number = app.flask_app.config['TWILIO_NUMBER']

client = TwilioRestClient(account=twilio_account_sid, token=twilio_auth_token)


@celery.task()
def send_sms_reminder(appointment_id):
    try:
        appointment = db.session.query(
            Appointment).filter_by(id=appointment_id).one()
    except NoResultFound:
        return

    time = arrow.get(appointment.time).to(appointment.timezone)
    body = "Hello {0}. You have an appointment at {1}!".format(
        appointment.name,
        time.format('h:mm a')
    )

    client.messages.create(
        body=body,
        to=appointment.phone_number,
        from_=twilio_number,
    )


# Using Djano
#########################################################################
from __future__ import unicode_literals

from twilio.rest import Client
from django.core.exceptions import MiddlewareNotUsed
import os
import logging
import json

logger = logging.getLogger(__name__)

MESSAGE = """[This is a test] ALERT! It appears the server is having issues.
Exception: %s. Go to: http://newrelic.com for more details."""

NOT_CONFIGURED_MESSAGE = """Cannot initialize Twilio notification
middleware. Required enviroment variables TWILIO_ACCOUNT_SID, or
TWILIO_AUTH_TOKEN or TWILIO_NUMBER missing"""


def load_admins_file():
    with open('config/administrators.json') as adminsFile:
        admins = json.load(adminsFile)
        return admins


def load_twilio_config():
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_NUMBER')

    if not all([twilio_account_sid, twilio_auth_token, twilio_number]):
        logger.error(NOT_CONFIGURED_MESSAGE)
        raise MiddlewareNotUsed

    return (twilio_number, twilio_account_sid, twilio_auth_token)


class MessageClient(object):
    def __init__(self):
        (twilio_number, twilio_account_sid,
         twilio_auth_token) = load_twilio_config()

        self.twilio_number = twilio_number
        self.twilio_client = Client(twilio_account_sid,
                                              twilio_auth_token)

    def send_message(self, body, to):
        self.twilio_client.messages.create(body=body, to=to,
                                           from_=self.twilio_number,
                                           # media_url=['https://demo.twilio.com/owl.png'])
                                           )


class TwilioNotificationsMiddleware(object):
    def __init__(self):
        self.administrators = load_admins_file()
        self.client = MessageClient()

    def process_exception(self, request, exception):
        exception_message = str(exception)
        message_to_send = MESSAGE % exception_message

        for admin in self.administrators:
            self.client.send_message(message_to_send, admin['phone_number'])

        logger.info('Administrators notified')

        return None
