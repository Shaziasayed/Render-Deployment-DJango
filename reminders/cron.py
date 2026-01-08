from django.utils import timezone
from .models import Reminder
from .twilio_utils import send_sms_to_number

def check_and_send_due_reminders():
    now = timezone.now()
    due_reminders = Reminder.objects.filter(status='pending', due_date__lte=now)
    for reminder in due_reminders:
        message = reminder.message or f"Payment Reminder: ₹{reminder.amount} is due now."
        ok, info = send_sms_to_number(reminder.customer.phone, message)
        if ok:
            reminder.status = 'sent'
            reminder.last_sent_at = timezone.now()
            reminder.save()
