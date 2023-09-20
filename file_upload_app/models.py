from pathlib import Path
from config.utils import format_filename
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.core.validators import FileExtensionValidator


def file_to_path(instance: 'UploadedFile', filename: str) -> str:
    """
    Generates the file path for an uploaded file.

    Args:
        instance (UploadedFile): The instance of the UploadedFile model.
        filename (str): The original name of the uploaded file.

    Returns:
        str: The formatted file path.

    """
    user_id = instance.user_id.id
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'{timestamp}_{filename}'
    return f'files/user_{user_id}/{filename}'


class UploadedFile(models.Model):
    """
    Model for storing uploaded files and related information.
    """
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    user_email = models.CharField(max_length=255, blank=True, null=True)
    file_path = models.FileField(
        upload_to=file_to_path,
        validators=[FileExtensionValidator(allowed_extensions=['py'])]
    )
    file_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, default='success')
    upload_date = models.DateTimeField(auto_now_add=True, db_index=True)
    update = models.DateTimeField(auto_now=True, db_index=True)
    is_new = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """
        Custom save method to set user_email and format file_name before saving.
        """
        self.user_email = self.user_id.email
        self.file_name = format_filename(Path(self.file_path.name).name)
        super().save(*args, **kwargs)
