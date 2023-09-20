from typing import Union
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from file_upload_app.models import UploadedFile
from code_verification_app.tasks import run_code_check

class RecheckFileView(APIView):
    """
    API View for rechecking a file for compliance with coding standards.

    Attributes:
        permission_classes (tuple): A tuple of permissions defining who can use this API.

    Methods:
        get(request, pk): GET request handler for rechecking a file.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk: int) -> Response:
        """
        GET request handler for rechecking a file.

        Args:
            request (Request): The request object.
            pk (int): The identifier of the file to recheck.

        Returns:
            Response: API response containing the operation status and message.

        Raises:
            HTTP_403_FORBIDDEN: If the user does not have access to the file.
            HTTP_404_NOT_FOUND: If the file with the specified identifier is not found.
        """
        try:
            file_instance = UploadedFile.objects.get(pk=pk)

            # Check if the current user has access to the file
            if file_instance.user_id != request.user:
                return Response(
                    {"detail": "You do not have access to this file."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Launch a background task to recheck the file
            run_code_check.delay(file_instance.id)

            return Response(
                {
                    "result": "ok",
                    "message": "File sent for recheck."
                },
                status=status.HTTP_200_OK
            )
        except UploadedFile.DoesNotExist:
            return Response(
                {
                    "result": "failed",
                    "message": "File not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
