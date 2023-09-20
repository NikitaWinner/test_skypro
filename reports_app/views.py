from django.views.generic import ListView
from code_verification_app.models import CodeCheck


class ReportListView(ListView):
    model = CodeCheck
    template_name = 'reports_app/report_results.html'
    context_object_name = 'code_checks'


