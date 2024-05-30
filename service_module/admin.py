from django.contrib import admin
from . import models


# Register your models here.


class LessonAdmin(admin.ModelAdmin):
    pass
    list_display = ['lesson_name', 'lesson_course', 'theoretical_unit', 'practical_units', 'lesson_type']
    list_editable = ['lesson_course', 'theoretical_unit', 'practical_units', 'lesson_type']


class PresentationAdmin(admin.ModelAdmin):
    pass
    list_display = ['lesson', 'teacher', 'capacity', 'for_semester', 'class_formation_time']
    list_editable = ['teacher', 'capacity', 'for_semester', 'class_formation_time']


class SemesterAdmin(admin.ModelAdmin):
    pass
    list_display = ['semester_number', 'is_main_semester', 'select_unit_permission', 'start_select_unit_time', 'end_select_unit_time']
    list_editable = ['is_main_semester', 'select_unit_permission', 'start_select_unit_time', 'end_select_unit_time']


admin.site.register(models.ExamTime)
admin.site.register(models.Lesson, LessonAdmin)
admin.site.register(models.Presentation, PresentationAdmin)
admin.site.register(models.Semester, SemesterAdmin)
admin.site.register(models.EducationGroup)
admin.site.register(models.Major)
admin.site.register(models.Requests)
admin.site.register(models.Payment)
admin.site.register(models.FixedTuition)
admin.site.register(models.VariableTuition)
admin.site.register(models.Bill)