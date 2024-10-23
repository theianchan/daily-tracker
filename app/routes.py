from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from app.utils.message_parser import MessageParser
from app.utils.spreadsheet import SpreadsheetManager
from app.config import Config
from datetime import datetime, timedelta
import pytz

bp = Blueprint("main", __name__)


def send_sms(message, to_number):
    client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    client.messages.create(body=message, from_=Config.TWILIO_PHONE_NUMBER, to=to_number)


@bp.route("/sms", methods=["POST"])
def incoming_sms():
    message_body = request.values.get("Body", "")
    from_number = request.values.get("From", "")

    # Check if it's a summary request
    parsed_data = MessageParser.parse_message(message_body)

    if parsed_data == "SUMMARY_REQUEST":
        spreadsheet = SpreadsheetManager()
        summary = spreadsheet.get_7day_summary()

        response = MessagingResponse()
        response.message(summary)
        return str(response)

    # Parse and save the data
    try:
        spreadsheet = SpreadsheetManager()
        spreadsheet.append_row(parsed_data.to_row())

        response = MessagingResponse()
        response.message("Data recorded successfully!")
        return str(response)

    except Exception as e:
        response = MessagingResponse()
        response.message("Sorry, I couldn't understand that message. Please try again.")
        return str(response)


def check_missing_data():
    """
    Scheduled job to check for missing data from previous day
    """
    current_hour = datetime.now(pytz.timezone(Config.TIMEZONE)).hour

    # Only run during the specified window
    if (
        current_hour < Config.REMINDER_START_HOUR
        or current_hour >= Config.REMINDER_END_HOUR
    ):
        return

    spreadsheet = SpreadsheetManager()
    yesterday = (datetime.now() - timedelta(days=1)).date()
    yesterday_data = spreadsheet.get_date_data(yesterday)

    if not yesterday_data or any(not field for field in yesterday_data[1:]):
        send_sms(
            "You haven't logged all your health data for yesterday. Please log your missing data!",
            "YOUR_PHONE_NUMBER",  # Replace with the user's phone number
        )


# Schedule the reminder job to run every REMINDER_INTERVAL minutes
from app import scheduler

scheduler.add_job(
    func=check_missing_data,
    trigger="interval",
    minutes=Config.REMINDER_INTERVAL,
    timezone=pytz.timezone(Config.TIMEZONE),
)


# Schedule weekly summary (e.g., every Monday at 9 AM)
def send_weekly_summary():
    spreadsheet = SpreadsheetManager()
    summary = spreadsheet.get_7day_summary()
    send_sms(summary, "YOUR_PHONE_NUMBER")  # Replace with the user's phone number


scheduler.add_job(
    func=send_weekly_summary,
    trigger="cron",
    day_of_week="mon",
    hour=9,
    timezone=pytz.timezone(Config.TIMEZONE),
)
