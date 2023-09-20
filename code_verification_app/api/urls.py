from django.urls import path
from .views import RecheckFileView

urlpatterns = [
    path('file/<int:pk>/', RecheckFileView.as_view(), name='recheck-file'),
]
