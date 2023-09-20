from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import UploadedFile


class UploadedFileForm(forms.ModelForm):
    """
    A form for uploading files along with optional descriptions.

    Attributes:
        file_path (FileField): The field for uploading files.
        description (CharField): A field for providing descriptions of the uploaded files.
    """

    class Meta:
        model = UploadedFile
        fields = ('file_path', 'description')
        labels = {
            'file_path': 'Путь до файла',
            'description': 'Описание',
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the UploadedFileForm.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.add_input(Submit('submit', 'Загрузить', css_class='btn btn-primary'))


class OverwriteFileForm(forms.ModelForm):
    """
    A form for overwriting existing files or creating new ones.

    Attributes:
        file_path (FileField): The field for uploading files.
        description (CharField): A field for providing descriptions of the uploaded files.
        file_id (IntegerField): A hidden field for storing the file's ID (for overwriting).
    """

    class Meta:
        model = UploadedFile
        fields = ['file_path', 'description', 'file_id']
        labels = {
            'file_path': 'Путь до файла',
            'description': 'Описание',
        }

    file_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        """
        Initialize the OverwriteFileForm.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.fields['file_path'].widget.attrs.update({'class': 'form-control-file'})
