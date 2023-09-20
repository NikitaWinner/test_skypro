import logging
from typing import List
from django.core.mail import send_mail
from code_verification_app.models import CodeCheck
from config.celery import app

logger = logging.getLogger(__name__)


@app.task
def send_notification_email() -> None:
    """
    Send email notifications for verified code checks.

    This task retrieves all code checks with a status of 'VERIFIED' and 'is_sent' set to False.
    It sends an email notification to the user associated with each code check and updates
    the 'is_sent' field to True for each sent notification.

    Returns:
        None
    """
    checks: List[CodeCheck] = CodeCheck.objects.filter(
        status=CodeCheck.Status.VERIFIED,
        is_sent=False
    ).all()

    for check in checks:
        try:
            # Send email notification
            send_mail(
                'Verification Report',
                f'File verification results: {check.result}',
                'melnov.nikita@gmail.com',
                [check.file_name.user_email],
                fail_silently=False,
            )

            # Log the email notification
            logger.info(f'Email notification sent to {check.file_name.user_email} for check ID {check.id}')

            # Mark the check as sent
            check.is_sent = True
            check.save()
        except Exception as e:
            # Log errors if email notification fails
            logger.error(f'Error sending email notification for check ID {check.id}: {str(e)}')
