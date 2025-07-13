from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_booking_confirmation(self, booking_id, user_email, booking_details):
    """
    Task to send a booking confirmation email
    
    Args:
        booking_id: ID of the booking
        user_email: Email address of the user who made the booking
        booking_details: Dictionary containing booking details
    """
    try:
        subject = f"Booking Confirmation #{booking_id}"
        
        # Prepare context for the email template
        context = {
            'booking_id': booking_id,
            'user_email': user_email,
            'check_in': booking_details.get('check_in'),
            'check_out': booking_details.get('check_out'),
            'total_price': booking_details.get('total_price'),
            'listing_title': booking_details.get('listing_title'),
            'number_of_guests': booking_details.get('number_of_guests'),
        }
        
        # Render HTML email
        html_message = render_to_string('emails/booking_confirmation.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Booking confirmation email sent for booking #{booking_id} to {user_email}")
        return f"Email sent to {user_email} for booking #{booking_id}"
        
    except Exception as exc:
        logger.error(f"Failed to send booking confirmation email: {str(exc)}")
        # Retry the task with exponential backoff
        raise self.retry(exc=exc)
