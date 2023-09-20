from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from file_upload_app.models import UploadedFile
from .serializers import UploadedFileSerializer, DetailFileSerializer


class UploadedFileViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing uploaded files.

    This viewset provides CRUD operations for uploaded files,
    including listing, creating, updating, and deleting files.

    Attributes:
        queryset (QuerySet): The queryset of UploadedFile objects.
        serializer_class (Serializer): The serializer class for UploadedFile objects.
        parser_classes (tuple): The parser classes for handling multipart and form data.

    Methods:
        retrieve(request, *args, **kwargs): Retrieve a single uploaded file.
    """

    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single uploaded file.

        Args:
            request (Request): The HTTP GET request.
            *args: Variable length argument list.
            **kwargs: Keyword arguments.

        Returns:
            Response: The response containing the detailed information of the file.
        """
        instance = self.get_object()
        serializer = DetailFileSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteFileView(DestroyAPIView):
    """
    A view for deleting an uploaded file.

    This view allows deleting an uploaded file by its ID.

    Attributes:
        queryset (QuerySet): The queryset of UploadedFile objects.
        serializer_class (Serializer): The serializer class for UploadedFile objects.
        lookup_field (str): The field to use for looking up the file by ID.
    """

    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    lookup_field = 'id'


class UpdateFileView(UpdateAPIView):
    """
    A view for updating an uploaded file.

    This view allows updating an uploaded file by its ID.

    Attributes:
        queryset (QuerySet): The queryset of UploadedFile objects.
        serializer_class (Serializer): The serializer class for UploadedFile objects.
        lookup_field (str): The field to use for looking up the file by ID.
    """

    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    lookup_field = 'id'
