from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('record-marks', views.RecordMarksPage.as_view(), name='record_mark_page'),
    path('record-marks/<presentation_id>', views.RecordMarksDetail.as_view(), name='record_mark_detail'),

    path('grade-appeal-list', views.TeacherGradeAppealList.as_view(), name='teacher_grade_appeal_list'),
    path('grade-appeal-detail/<appeal_id>', views.TeacherGradeAppealDetail.as_view(), name='teacher_grade_appeal_detail'),
]
