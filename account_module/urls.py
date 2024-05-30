from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('student/login', views.StudentLoginPage.as_view(), name='student_login'),
    path('staff-teacher/login', views.StaffTeacherLoginPage.as_view(), name='staff_teacher_login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('change-password', views.ChangePasswordView.as_view(), name='change_password'),
    path('user-profile', views.UserInformationView.as_view(), name='user_profile'),
    path('edit-profile', views.EditUserProfilePage.as_view(), name='edit_profile'),
]
