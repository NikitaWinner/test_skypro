import subprocess
import tempfile
import os
from django.utils import timezone
from code_verification_app.models import CodeCheck
from file_upload_app.models import UploadedFile
from typing import Dict, Union, List


class CodeCheckerFlake:
    """
    Class for code verification using flake8 and saving the verification results in the CodeCheck model.

    Args:
        uploaded_file (UploadedFile): The UploadedFile object to be checked.

    Attributes:
        uploaded_file (UploadedFile): The UploadedFile object to be checked.

    """
    def __init__(self, uploaded_file: UploadedFile) -> None:
        """
        Initialize a new CodeCheckerFlake instance.

        Args:
            uploaded_file (UploadedFile): The UploadedFile object to be checked.

        """
        self.uploaded_file = uploaded_file

    def run_check(self) -> None:
        """
        Perform code verification using flake8 and save the results in the CodeCheck model.

        Raises:
            subprocess.CalledProcessError: If the flake8 process exits with a non-zero return code.

        """
        file_path: str = self.uploaded_file.file_path.path

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path: str = os.path.join(temp_dir, os.path.basename(file_path))
            with open(file_path, 'rb') as original_file:
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(original_file.read())

            result: subprocess.CompletedProcess[Union[bytes, str]] = subprocess.run(
                ['flake8', temp_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

        output_lines: List[str] = result.stdout.splitlines()
        other_messages: List[str] = []

        for line in output_lines:
            other_messages.append(line)

        mes_res: Dict[str, Union[str, List[Dict[str, str]]]] = {
            'comment': []
        }

        for message in other_messages:
            message_list: List[str] = message.split(':')
            num_line: str = message_list[2]
            start: int = message_list.index(num_line)
            comment: str = ''.join(message_list[start + 2:])
            mes_res['comment'].append({f'line {num_line}': comment})

        code_check, created = CodeCheck.objects.get_or_create(
            file_name=self.uploaded_file,
            defaults={
                'created_at': timezone.now(),
                'status': CodeCheck.Status.VERIFIED,
            }
        )
        code_check.result = mes_res
        code_check.save()
        self.uploaded_file.is_new = False
        self.uploaded_file.save()
