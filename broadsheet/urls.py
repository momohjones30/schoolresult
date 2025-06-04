from django.urls import path
from .views import (
    session_list, term_list, grade_list, broadsheet_view,
    DownloadBroadsheetPDF, DownloadBroadsheetExcel
)

urlpatterns = [
    path('', session_list, name='session_list'),
    path('session/<int:session_id>/terms/', term_list, name='term_list'),
    path('session/<int:session_id>/term/<int:term_id>/grades/', grade_list, name='grade_list'),
    path('session/<int:session_id>/term/<int:term_id>/grade/<int:grade_id>/', broadsheet_view, name='broadsheet_view'),
    path('session/<int:session_id>/term/<int:term_id>/grade/<int:grade_id>/pdf/', DownloadBroadsheetPDF.as_view(), name='download_pdf'),
    path('session/<int:session_id>/term/<int:term_id>/grade/<int:grade_id>/excel/', DownloadBroadsheetExcel.as_view(), name='download_excel'),
]