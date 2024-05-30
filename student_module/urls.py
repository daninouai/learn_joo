from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('current-semester-status', views.CurrentSemesterStatusPageView.as_view(), name='current_semester_status'),

    path('student-requests', views.StudentsRequestsPageView.as_view(), name='student_requests'),
    path('student-payments', views.StudentPaymentsPageView.as_view(), name='student_payments'),
    path('student-manage-payments', views.StudentManagePaymentsPageView.as_view(), name='student_manage_payments'),

    path('evaluation-teacher', views.EvaluationOfTeacherPageView.as_view(), name='evaluation_teacher'),
    path('do-evaluation-teacher/<presentation_id>', views.EvaluationOfStudentDetailView.as_view(), name='do_evaluation_teacher'),

    path('student-report-card', views.StudentReportCardView.as_view(), name='student_report_card'),
    path('student-grade-appeal', views.StudentGradeAppealPage.as_view(), name='student_grade_appeal_page'),
    path('student-do-grade-appeal/<mark_id>', views.StudentGradeAppealDetail.as_view(), name='student_grade_appeal_detail'),

]
