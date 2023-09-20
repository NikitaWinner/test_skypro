from rest_framework import serializers
from file_upload_app.models import UploadedFile
from code_verification_app.models import CodeCheck
from config.utils import format_filename
from typing import List


class TrimmedFileNameSerializer(serializers.CharField):
    """
    A custom serializer for formatting file names.

    This serializer is used to format file names by trimming extra spaces.

    Attributes:
        - value: The input file name.

    Returns:
        - str: The formatted file name.
    """

    def to_representation(self, value: str) -> str:
        return format_filename(value)


class DateTimeSerializer(serializers.DateTimeField):
    """
    A custom serializer for formatting date and time.

    This serializer is used to format date and time in 'YYYY-MM-DD HH:MM' format.

    Attributes:
        - value: The input datetime value.

    Returns:
        - str: The formatted date and time string.
    """

    def to_representation(self, value: datetime) -> str:
        return value.strftime('%Y-%m-%d %H:%M')


class CodeCheckSerializer(serializers.ModelSerializer):
    """
    Serializer for the CodeCheck model.

    This serializer is used to serialize CodeCheck objects.

    Attributes:
        - created_at: A DateTimeSerializer instance for formatting the 'created_at' field.

    Meta:
        - model: CodeCheck
        - fields: ('status', 'created_at', 'result')
    """
    created_at = DateTimeSerializer()

    class Meta:
        model = CodeCheck
        fields = ('status', 'created_at', 'result')


class DetailFileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UploadedFile model with detailed information.

    This serializer is used to serialize UploadedFile objects with detailed information, including CodeCheck objects.

    Attributes:
        - checks: A list of CodeCheckSerializer instances for formatting the 'code_checks' field.
        - update: A DateTimeSerializer instance for formatting the 'update' field.
        - file_name: A TrimmedFileNameSerializer instance for formatting the 'file_name' field.

    Meta:
        - model: UploadedFile
        - fields: ('id', 'file_name', 'update', 'status', 'checks')
    """
    checks = CodeCheckSerializer(many=True, read_only=True, source='code_checks')
    update = DateTimeSerializer()
    file_name = TrimmedFileNameSerializer()

    class Meta:
        model = UploadedFile
        fields = ('id', 'file_name', 'update', 'status', 'checks')


class UploadedFileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UploadedFile model.

    This serializer is used to serialize UploadedFile objects.

    Attributes:
        - update: A DateTimeSerializer instance for formatting the 'update' field.
        - upload_date: A DateTimeSerializer instance for formatting the 'upload_date' field.
        - file_name: A TrimmedFileNameSerializer instance for formatting the 'file_name' field.

    Meta:
        - model: UploadedFile
        - fields: ['id', 'file_name', 'description', 'user_id', 'user_email', 'upload_date', 'update']
    """
    update = DateTimeSerializer()
    upload_date = DateTimeSerializer()
    file_name = TrimmedFileNameSerializer()

    class Meta:
        model = UploadedFile
        fields = ['id', 'file_name', 'description', 'user_id', 'user_email', 'upload_date', 'update']
