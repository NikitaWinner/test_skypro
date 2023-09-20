from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import UploadedFile
from .forms import UploadedFileForm, OverwriteFileForm
from code_verification_app.service import CodeCheckerFlake


@method_decorator(login_required, name='dispatch')
class FileUploadView(CreateView):
    """
    View for uploading files.

    Attributes:
        model (UploadedFile): The model to use for the view.
        form_class (UploadedFileForm): The form class for file upload.
        template_name (str): The name of the template to render.
        success_url (str): The URL to redirect to after a successful upload.
    """
    model = UploadedFile
    form_class = UploadedFileForm
    template_name = 'file_upload_app/upload_file.html'
    success_url = reverse_lazy('file_upload_app:upload_file')

    def form_valid(self, form: UploadedFileForm) -> HttpResponseRedirect:
        """
        Handles form submission when it is valid.

        Args:
            form (UploadedFileForm): The form object containing the uploaded file.

        Returns:
            HttpResponseRedirect: Redirects to the success URL.
        """
        form.instance.user_id = self.request.user
        # file = form.save()
        # check = CodeCheckerFlake(file)
        # check.run_check()
        return super().form_valid(form)


class MyFilesView(ListView):
    """
    View to display a list of user's uploaded files.

    Attributes:
        model (UploadedFile): The model to use for the view.
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the variable to use in the template for the file list.
    """
    model = UploadedFile
    template_name = 'file_upload_app/my_files.html'
    context_object_name = 'files'

    def get_queryset(self):
        """
        Returns the queryset of UploadedFile objects for the current user.

        Returns:
            QuerySet: The queryset of uploaded files for the user.
        """
        return UploadedFile.objects.filter(user_id=self.request.user)


class DeleteFileView(DeleteView):
    """
    View to delete an uploaded file.

    Attributes:
        model (UploadedFile): The model to use for the view.
        template_name (str): The name of the template to render for file deletion.
        success_url (str): The URL to redirect to after a successful file deletion.
    """
    model = UploadedFile
    template_name = 'file_upload_app/confirm_delete.html'
    success_url = reverse_lazy('file_upload_app:my_files')

    def get_queryset(self):
        """
        Returns the queryset of UploadedFile objects for the current user.

        Returns:
            QuerySet: The queryset of uploaded files for the user.
        """
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user)


class OverwriteFileView(UpdateView):
    """
    View to overwrite an existing uploaded file.

    Attributes:
        model (UploadedFile): The model to use for the view.
        form_class (OverwriteFileForm): The form class for file overwrite.
        template_name (str): The name of the template to render for file overwrite.
        success_url (str): The URL to redirect to after a successful file overwrite.
    """
    model = UploadedFile
    form_class = OverwriteFileForm
    template_name = 'file_upload_app/overwrite_file.html'
    success_url = reverse_lazy('file_upload_app:my_files')

    def get_object(self, queryset=None):
        """
        Retrieves the UploadedFile object to be overwritten.

        Args:
            queryset: A queryset to filter the object.

        Returns:
            UploadedFile: The object to be overwritten.
        """
        file_id = self.kwargs.get('pk')
        return get_object_or_404(UploadedFile, pk=file_id)

    def form_valid(self, form: OverwriteFileForm) -> HttpResponseRedirect:
        """
        Handles form submission when it is valid.

        Args:
            form (OverwriteFileForm): The form object containing the updated file information.

        Returns:
            HttpResponseRedirect: Redirects to the success URL.
        """
        new_file = form.cleaned_data['file_path']
        if new_file:
            self.object.file_path = new_file
        self.object.description = form.cleaned_data['description']
        self.object.update = timezone.now()

        user = self.request.user if self.request.user.is_authenticated else None

        if user:
            self.object.user_id = user
            self.object.user_email = user.email

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
