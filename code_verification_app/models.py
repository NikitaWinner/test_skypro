from django.db import models
from file_upload_app.models import UploadedFile


class CodeCheck(models.Model):
    """
    Model to store information about code checks for files.

    Attributes:
        file_name (UploadedFile): ForeignKey to relate the check with the uploaded file.
        status (str): The status of the check, chosen from the `Status.choices` list.
        created_at (datetime): The date and time when the check record was created.
        is_sent (bool): A flag indicating whether a notification has been sent to the user.
        result (dict): The results of the code check in JSON format.

    Methods:
        __str__: Returns a string representation of the object.
    """

    class Status(models.TextChoices):
        """
        Class to define possible check statuses.
        """
        PROGRESS = 'In progress', 'Sent for testing'
        VERIFIED = 'Verified!', 'Check completed successfully'
        FAILED = 'Failed', 'Unsuccessful'

    file_name = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name='code_checks',
        verbose_name='Uploaded file',
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PROGRESS,
        verbose_name='Check status',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date and time of creation',
    )
    is_sent = models.BooleanField(
        default=False,
        verbose_name='Notification sent',
    )
    result = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        verbose_name='Code check results',
    )

    def __str__(self) -> str:
        return f'Check for file: {self.file_name}'
