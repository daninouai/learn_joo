from django.db.models import Prefetch
from django.http import HttpRequest
from django.views.generic import View, ListView
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from service_module.models import Presentation, Semester
from student_module.models import Marks, StudentGradeAppeal
from teacher_module.forms import StudentGradeAppealResponseForm


# Create your views here.


class RecordMarksPage(View):
    def get(self, request: HttpRequest):
        current_semester = Semester.objects.filter(is_main_semester=True).first()
        lessons = Presentation.objects.filter(teacher=request.user, for_semester=current_semester)
        context = {
            'lessons': lessons,
        }
        return render(request, 'teacher_module/record_marks_page.html', context)


class RecordMarksDetail(View):
    def get(self, request: HttpRequest, presentation_id):
        presentation = Presentation.objects.get(id=presentation_id)
        if presentation.teacher == request.user:
            students = presentation.student.all().order_by('user__last_name').prefetch_related(
                Prefetch('marks_set', queryset=Marks.objects.filter(for_semester__is_main_semester=True, presentation=presentation), to_attr='current_semester_marks')
            )

            merged_data = []
            for student in students:
                if student.current_semester_marks:
                    merged_data.append([student, student.current_semester_marks[0].mark])
                else:
                    merged_data.append([student, None])

            context = {
                'lessons': presentation,
                'students': students,
                'merged_data': merged_data,
            }
            return render(request, 'teacher_module/record_marks_detail.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request: HttpRequest, presentation_id):
        presentation = Presentation.objects.get(id=presentation_id)
        if presentation.teacher == request.user:
            marks = request.POST.getlist('marks')
            students = presentation.student.all().order_by('user__last_name')
            current_semester = Semester.objects.filter(is_main_semester=True).first()
            for index, student in enumerate(students):
                if not Marks.objects.filter(for_semester=current_semester, for_student=student, presentation=presentation).exists() and marks[index]:
                    Marks.objects.create(for_semester=current_semester, for_student=student, presentation=presentation, mark=marks[index])
                elif marks[index]:
                    mark = Marks.objects.filter(for_semester=current_semester, for_student=student, presentation=presentation)
                    mark.update(mark=marks[index])

            messages.success(request, 'نمرات کلاس با موفقیت ثبت شد.')
            return redirect(reverse('record_mark_page'))
        else:
            return HttpResponseForbidden()


class TeacherGradeAppealList(ListView):
    model = StudentGradeAppeal
    template_name = 'teacher_module/teacher_grade_appeal_list.html'
    context_object_name = 'student_grade_appeal_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(mark__presentation__teacher=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unresponded_appeals = self.get_queryset().filter(is_response=False)
        responded_appeals = self.get_queryset().filter(is_response=True)
        context['unresponded_appeals'] = unresponded_appeals
        context['responded_appeals'] = responded_appeals
        return context


class TeacherGradeAppealDetail(View):
    def get(self, request: HttpRequest, appeal_id):
        get_appeal = StudentGradeAppeal.objects.get(id=appeal_id)
        form = StudentGradeAppealResponseForm(instance=get_appeal)
        context = {
            'get_appeal': get_appeal,
            'form': form,
        }
        return render(request, 'teacher_module/teacher_grade_appeal_detail.html', context)

    def post(self, request: HttpRequest, appeal_id):
        get_appeal = StudentGradeAppeal.objects.get(id=appeal_id)
        form = StudentGradeAppealResponseForm(request.POST, instance=get_appeal)
        if form.is_valid():
            form.instance.is_response = True
            form.save()
            messages.success(request, 'پاسخ به اعتراض با موفقیت ثبت شد.')
            return redirect(reverse('teacher_grade_appeal_list'))
        else:
            context = {
                'get_appeal': get_appeal,
                'form': form,
            }
            return render(request, 'teacher_module/teacher_grade_appeal_detail.html', context)
