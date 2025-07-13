from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_listing_notification(listing_id, listing_title):
    """
    Task to send an email notification when a new listing is created
    """
    logger.info(f"Sending notification for new listing: {listing_title} (ID: {listing_id})")
    
    subject = f"New Listing: {listing_title}"
    message = f"A new listing has been created with ID: {listing_id} and title: {listing_title}"
    
    # This is a mock function that would normally send an email
    # In a real application, you would use Django's send_mail function
    logger.info(f"Email notification sent for listing: {listing_title}")
    
    return f"Notification sent for listing {listing_id}"
