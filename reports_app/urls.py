from django.urls import path
from . import views


app_name = 'reports_app'

urlpatterns = [
    path('results/', views.ReportListView.as_view(), name='results'),
]