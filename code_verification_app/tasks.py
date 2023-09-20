from celery import shared_task
from typing import List

from file_upload_app.models import UploadedFile
from .service import CodeCheckerFlake
from email_notification_app.tasks import send_notification_email


@shared_task
def run_code_check() -> None:
    """
    Asynchronous task for checking code in uploaded files and sending notifications.

    Retrieves a list of newly uploaded files, performs code checking for each of them, and then
    triggers an asynchronous task to send notifications.

    """
    files_to_check: List[UploadedFile] = UploadedFile.objects.filter(is_new=True).all()
    for uploaded_file in files_to_check:
        code_check = CodeCheckerFlake(uploaded_file)
        code_check.run_check()

    send_notification_email.delay()
