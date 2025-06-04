from django.urls import path
# from .views import (
#         student_sessions,
#         student_terms,
#         student_grades,
#         student_results,
#         student_login,
#         student_logout,

#         student_dashboard,
#         session_terms,
#         grade_performance,
#     )

# Every in this bulk for students dashboard

'''urlpatterns = [
        path('student/sessions', student_sessions, name='student_sessions'),
        path('student/sessions/<int:session_id>/terms/', student_terms, name='student_terms'),
        path('student/terms/<int:term_id>/grades/', student_grades, name='student_grades'),
        path('student/grades/<int:grade_id>/results/', student_results, name='student_results'),
        path('student/login/', student_login, name='student_login'),
        path('student/logout/', student_logout, name='student_logout'),

    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('dashboard/session/<int:session_id>/', session_terms, name='session_terms'),
    path('dashboard/grade/<int:grade_id>/', grade_performance, name='grade_performance'),
]
'''
from . import views

urlpatterns = [
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),  
    path('sessions/<int:session_id>/terms/', 
         views.session_terms, name='session_terms'),
    path('sessions/<int:session_id>/terms/<int:term_id>/grades/', 
         views.term_grades, name='term_grades'),
    path('sessions/<int:session_id>/terms/<int:term_id>/grades/<int:grade_id>/performance/', 
         views.grade_performance, name='grade_performance'),
]
