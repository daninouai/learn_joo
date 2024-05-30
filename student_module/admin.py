from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Student)
admin.site.register(models.EvaluationByStudent)
admin.site.register(models.Marks)
admin.site.register(models.SemesterGPA)
admin.site.register(models.StudentGradeAppeal)