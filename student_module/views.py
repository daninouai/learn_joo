from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpRequest, HttpResponse, HttpResponseForbidden
from service_module.models import Presentation, Semester, Lesson, Requests, Payment, Bill, VariableTuition
import uuid
from django.urls import reverse
from django.shortcuts import get_object_or_404

from student_module.models import EvaluationByStudent, SemesterGPA, Marks, StudentGradeAppeal
from utils.student_services import calculate_gpa, calculate_fixed_tuition
from .forms import StudentRequestsForm, StudentPresentationForm, StudentGradeAppealForm
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import requests
import json
from collections import defaultdict
from django.contrib import messages
from datetime import datetime
from django.utils import timezone


# Create your views here.


def calculate_gpa_task(request):
    user = request.user
    student_semesters = user.registered_semesters.all()
    for semester in student_semesters:
        marks = Marks.objects.filter(for_semester=semester, for_student=request.user)
        result = calculate_gpa(marks)
        obtained_units, passed_units, rejected_units, avg_marks = result

        last_gpa = SemesterGPA.objects.filter(for_student=user)
        total_gpa = 0
        if last_gpa:
            for gpa in last_gpa:
                total_gpa = gpa.semester_GPA

        user.gpa = total_gpa
        user.units_obtained = obtained_units
        user.units_passed = passed_units
        user.units_rejected = rejected_units
        user.semester_passed = student_semesters.count()
        user.save()

        semester_gpa, created = SemesterGPA.objects.get_or_create(
            for_student=user,
            semester=semester,
            defaults={
                'semester_GPA': avg_marks,
                'total_GPA': total_gpa,
                'obtained_units': obtained_units,
                'passed_units': passed_units,
                'rejected_units': rejected_units
            }
        )

        if not created:
            semester_gpa.semester_GPA = avg_marks
            semester_gpa.total_GPA = total_gpa
            semester_gpa.obtained_units = obtained_units
            semester_gpa.passed_units = passed_units
            semester_gpa.rejected_units = rejected_units
            semester_gpa.save()

        for mark in marks:
            semester_gpa.mark.add(mark)
    pass


class CurrentSemesterStatusPageView(View):
    def get(self, request: HttpRequest):
        current_semester = Semester.objects.filter(is_main_semester=True).first()
        lessons = Presentation.objects.filter(for_semester=current_semester, student=request.user)
        last_semester = request.user.registered_semesters.last()

        context = {
            'lessons': lessons,
            'last_semester': last_semester,
        }
        return render(request, 'service_module/current_semester_status_page.html', context)


class StudentsRequestsPageView(View):
    def get(self, request: HttpRequest):
        user_requests = Requests.objects.filter(for_student=request.user)
        request_form = StudentRequestsForm()

        context = {
            'request_form': request_form,
            'user_requests': user_requests,
        }
        return render(request, 'student_module/student_requests_page.html', context)

    def post(self, request: HttpRequest):
        request_form = StudentRequestsForm(request.POST)
        current_semester = Semester.objects.filter(is_main_semester=True).first()
        if request_form.is_valid():
            request_type = request_form.cleaned_data['request_type']
            request_text = request_form.cleaned_data['request_text']
            if request_type == 'permission_select_unit':
                print(request.user.registered_semesters.all())
                if current_semester not in request.user.registered_semesters.all():
                    amount = calculate_fixed_tuition(request.user)
                    if amount <= 0:
                        return HttpResponseForbidden()
                    request.user.amount_payable += amount
                    request.user.save()
                    Bill.objects.create(for_semester=current_semester, for_student=request.user, type='fixed_tuition', amount=amount)
                    Requests.objects.create(request_type=request_type, request_text=request_text, for_student=request.user, for_semester=current_semester, status='confirmed')
                    request.user.registered_semesters.add(current_semester)
                    messages.success(request, 'درخواست شما با موفقیت ثبت شد.')
                else:
                    messages.error(request, 'این درخواست در ترم جاری از قبل ثبت شده است.')
            else:
                Requests.objects.create(request_type=request_type, request_text=request_text, for_student=request.user, for_semester=current_semester, status='pending')
                messages.success(request, 'درخواست شما با موفقیت ثبت شد.')
        return redirect(reverse('student_requests'))


class StudentManagePaymentsPageView(View):
    def get(self, request: HttpRequest):
        student_payments = Payment.objects.filter(for_student=request.user)
        bills = Bill.objects.filter(for_student=request.user)
        user = request.user
        context = {
            'student_payments': student_payments,
            'user': user,
            'bills': bills,
        }
        return render(request, 'student_module/student_payments_page.html', context)


class EvaluationOfTeacherPageView(View):
    def get(self, request: HttpRequest):
        current_semester = Semester.objects.filter(is_main_semester=True).first()

        lessons_without_evaluation = Presentation.objects.filter(student=request.user, for_semester=current_semester).exclude(evaluationbystudent__for_student__isnull=False)
        lessons_with_evaluation = Presentation.objects.filter(student=request.user, for_semester=current_semester).exclude(evaluationbystudent__for_student__isnull=True)

        context = {
            'lessons_without_evaluation': lessons_without_evaluation,
            'lessons_with_evaluation': lessons_with_evaluation,
        }
        return render(request, 'student_module/evaluation_of_teacher.html', context)


class StudentReportCardView(View):
    def get(self, request: HttpRequest):
        student = request.user
        calculate_gpa_task(request)
        semester_gaps = SemesterGPA.objects.filter(for_student=student)
        context = {
            'user_base': student.user,
            'user': student,
            'semester_gaps': semester_gaps,
        }
        return render(request, 'student_module/student_report_card_detail.html', context)


class StudentGradeAppealPage(View):
    def get(self, request: HttpRequest):
        marks = Marks.objects.filter(for_student=request.user, for_semester__is_main_semester=True, studentgradeappeal__for_student__isnull=True).distinct()
        graded_marks = StudentGradeAppeal.objects.filter(semester__is_main_semester=True, for_student=request.user)
        context = {
            'marks': marks,
            'graded_marks': graded_marks,
        }
        return render(request, 'student_module/student_grade_appeal_page.html', context)


class StudentGradeAppealDetail(View):
    def get(self, request: HttpRequest, mark_id):
        mark = get_object_or_404(Marks, for_student=request.user, id=mark_id)
        form = StudentGradeAppealForm()
        context = {
            'mark': mark,
            'form': form,
        }
        return render(request, 'student_module/student_grade_appeal_detail.html', context)

    def post(self, request: HttpRequest, mark_id):
        mark = get_object_or_404(Marks, for_student=request.user, id=mark_id)
        form = StudentGradeAppealForm(request.POST)
        if form.is_valid():
            form.instance.for_student = request.user
            form.instance.mark = mark
            form.instance.semester = Semester.objects.filter(is_main_semester=True).first()
            form.save()
            return redirect(reverse('student_grade_appeal_page'))
        else:
            context = {
                'mark': mark,
                'form': form,
            }
            return render(request, 'student_module/student_grade_appeal_detail.html', context)


class EvaluationOfStudentDetailView(View):
    def get(self, request: HttpRequest, presentation_id):
        get_presentation = Presentation.objects.get(id=presentation_id)
        check_evaluation = EvaluationByStudent.objects.filter(for_student=request.user, presentation=get_presentation).exists()
        if not check_evaluation:
            form = StudentPresentationForm()
            context = {
                'lesson': get_presentation,
                'form': form,
            }
            return render(request, 'student_module/evaluation_of_teacher_detail.html', context)
        return HttpResponseForbidden()

    def post(self, request: HttpRequest, presentation_id):
        get_presentation = Presentation.objects.get(id=presentation_id)
        check_evaluation = EvaluationByStudent.objects.filter(for_student=request.user, presentation=get_presentation).exists()
        if not check_evaluation:
            form = StudentPresentationForm(request.POST)
            form.instance.presentation = get_presentation
            form.instance.for_student = request.user
            if form.is_valid():
                form.save()
                messages.success(request, 'ارزیابی استاد با موفقیت ثبت شد.')
                return redirect(reverse('evaluation_teacher'))
            else:
                context = {
                    'lesson': get_presentation,
                    'form': form,
                }
                return render(request, 'student_module/evaluation_of_teacher_detail.html', context)
        else:
            return HttpResponseForbidden()


class StudentPaymentsPageView(View):
    def get(self, request: HttpRequest):
        student_payments = Payment.objects.filter(for_student=request.user)
        user = request.user

        fixed_tuition = Bill.objects.filter(for_student=user, type='fixed_tuition')
        variable_tuition = Bill.objects.filter(for_student=user, type='variable_tuition')

        merged_data = defaultdict(list)
        all_tuition_merged = []

        for tuition in fixed_tuition:
            merged_data[tuition.for_semester].append(tuition)

        for tuition in variable_tuition:
            merged_data[tuition.for_semester].append(tuition)

        for semester, tuition in merged_data.items():
            all_tuition_merged.append(tuition)

        context = {
            'student_payments': student_payments,
            'user': user,
            'merged_data': all_tuition_merged,
        }
        return render(request, 'student_module/student_manage_payments_page.html', context)
