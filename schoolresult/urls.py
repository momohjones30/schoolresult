from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .admin import studentsite
from . import views
from subjects.views import subject_sessions, session_terms, term_grades, grade_scores, save_scores #subjectgrade_subjects, get_scores
from django.urls import include

urlpatterns = [
    path('', views.main_page, name='main_page'),  # for front page
    path('admin/', admin.site.urls), # for main admin
    #path('staff/', staffadminsite.urls), #staff portal
    path('studentadmin/', studentsite.urls), #student portal
    path('useregister/', views.register, name='register'),  # URL for USER REGISTRATION which automatically logs them in
    path('student_registration/', views.student_registration, name='student_registration'),  # URL for STUDENT REGISTRATION

    #path('teacher_registration/', views.student_registration, name='teacher_registration'),  # URL for STUDENT REGISTRATION
    path('teacherlogin/', views.teacher_login, name='teacher_login'), # for teacherlogin
    path('teacherlogout/', views.teacher_logout, name='logout'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'), #for loggedin teacher's dashboard
    path('sessions/<int:subject_id>/', views.sessionlist, name='sessionlist'),

    path('terms/<int:session_id>/', views.term_list, name='term_list'),
    path('grades/<int:term_id>/', views.grade_list, name='grade_list'),
    path('scores/<int:grade_id>/', views.student_scores, name='student_scores'),


  


    path('subject/<int:subject_id>/sessions/', subject_sessions, name='subject_sessions'),
    path('subject/<int:subject_id>/session/<int:session_id>/terms/', session_terms, name='session_terms'),
    path('subject/<int:subject_id>/session/<int:session_id>/term/<int:term_id>/grades/', term_grades, name='term_grades'),
    path('subject/<int:subject_id>/session/<int:session_id>/term/<int:term_id>/grade/<int:grade_id>/scores/', grade_scores, name='grade_scores'),
    path('save-scores/', save_scores, name='save_scores'),



 
    path('student/', include('student.urls')),

    path('promotion/', include('results.urls')),

    path('broadsheet/', include('broadsheet.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)