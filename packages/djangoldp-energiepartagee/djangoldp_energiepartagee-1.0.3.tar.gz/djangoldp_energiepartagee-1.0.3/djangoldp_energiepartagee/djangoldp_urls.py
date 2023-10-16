"""djangoldp uploader URL Configuration"""

from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from djangoldp_energiepartagee.views import ExportContributions, ExportContributionsAll, GeneratePdfCall, GeneratePdfReceipt, ContributionsCallView, ContributionsReminderView, ContributionsVentilationView

urlpatterns = [
    path('contributions/call/', csrf_exempt(ContributionsCallView.as_view()), name='contributions-call'),
    path('contributions/reminder/', csrf_exempt(ContributionsReminderView.as_view()), name='contributions-reminder'),
    path('contributions/ventilation/', csrf_exempt(ContributionsVentilationView.as_view()), name='contributions-ventilation'),
    path('contributions/call_pdf/<int:pk>/', csrf_exempt(GeneratePdfCall.as_view()), name="generate_callpdf_fromhtml"),
    path('contributions/receipt_pdf/<int:pk>/', csrf_exempt(GeneratePdfReceipt.as_view()), name="generate_receiptpdf_fromhtml"),
    path('contributions/csv/', csrf_exempt(ExportContributions.as_view()), name='export_contributions'),
    path('contributions/csv_all/', csrf_exempt(ExportContributionsAll.as_view()), name='export_contributions'),
]