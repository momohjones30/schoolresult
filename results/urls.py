from django.urls import path
from . import views

urlpatterns = [
    path('promotion/', views.promotion_home, name='promotion_home'),
    path('promotion/session/<int:session_id>/grades/', views.session_grades, name='session_grades'),
    path('promotion/grade/<int:grade_id>/students/', views.grade_students, name='grade_students'),
    path('promotion/students/new-session/', views.new_session_selection, name='new_session_selection'),
    path('promotion/students/new-grades/<int:session_id>/', views.new_grade_selection, name='new_grade_selection'),
    path('promotion/promote-students/', views.promote_students, name='promote_students'),
    path('promotionsuccess//', views.promotionsuccess, name='promotionsuccess'),
]