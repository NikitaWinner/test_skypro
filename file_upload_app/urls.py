from django.urls import path
from . import views


app_name = 'file_upload_app'

urlpatterns = [
    path('upload/', views.FileUploadView.as_view(), name='upload_file'),
    path('my-files/', views.MyFilesView.as_view(), name='my_files'),
    path('delete-file/<int:pk>/', views.DeleteFileView.as_view(), name='delete_file'),
    path('overwrite-file/<int:pk>/', views.OverwriteFileView.as_view(), name='overwrite_file'),

]