# backened/twilio_utils.py
import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_sms_to_number(phone_number, message):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

    if not all([account_sid, auth_token, twilio_number]):
        print("❌ Missing Twilio environment variables")
        return False, "Missing credentials"
    phone_number = phone_number.strip()  # remove spaces
    if not phone_number.startswith("+"):
        phone_number = "+91" + phone_number

    try:
        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            body=message,
            from_=twilio_number,
            to=phone_number
        )
        print("✅ SMS SENT")
        print("SID:", msg.sid)
        print("BODY:", message)
        return True, msg.sid

    except Exception as e:
        print("❌ SMS FAILED:", str(e))
        return False, str(e)
