from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from account_module.models import User
from dateutil.relativedelta import relativedelta


# from service_module.models import Semester, Presentation


# Create your models here.


class Student(AbstractBaseUser):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')

    class EducationStatusType(models.TextChoices):
        STUDYING = 'studying', 'در حال تحصیل'
        GRADUATED = 'graduated', 'فارغ التحصیل'

    class TypeOfAdmission(models.TextChoices):
        BY_TEST = 'by_test', 'با آزمون'
        NO_TEST = 'no_test', 'بدون آزمون'

    student_number = models.CharField(max_length=200, unique=True, verbose_name='شماره دانشجویی')
    education_status = models.CharField(max_length=200, choices=EducationStatusType.choices, verbose_name='وضعیت تحصیلی', db_column='education_status_en')
    gpa = models.FloatField(default=0, verbose_name='معدل دانشجو')
    units_obtained = models.FloatField(default=0, verbose_name='تعداد واحد های اخذ شده')
    units_passed = models.FloatField(default=0, verbose_name='تعداد واحد های گذرانده شده')
    units_rejected = models.FloatField(default=0, verbose_name='تعداد واحد های رد شده')
    semester_passed = models.IntegerField(default=0, verbose_name='سنوات (ترم) گذرانده')
    semesters_conditional = models.IntegerField(default=0, verbose_name='تعداد نیم سال های مشروطی')
    start_date_of_study = models.DateField(verbose_name='تاریخ شروع تحصیل')
    deadline_date_of_study = models.DateField(null=True, blank=True, verbose_name='تاریخ آخرین مهلت پایان تحصیل')
    last_updated_date = models.DateField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    major = models.ForeignKey('service_module.Major', on_delete=models.CASCADE, verbose_name='رشته تحصیلی', null=True)
    admission = models.CharField(max_length=200, choices=TypeOfAdmission.choices, verbose_name='نوع پذیرش', null=True, db_column='admission_en')
    admission_semester = models.ForeignKey('service_module.Semester', on_delete=models.CASCADE, verbose_name='نیم سال پذیرش', null=True)
    registered_semesters = models.ManyToManyField('service_module.Semester', related_name='registered_semesters_set', verbose_name='نیم سال های ثبت شده', blank=True)
    financial_balance = models.SmallIntegerField(default=0, verbose_name='تراز مالی', null=True)
    amount_payable = models.SmallIntegerField(default=0, verbose_name='قابل پرداخت', null=True)
    amount_paid = models.SmallIntegerField(default=0, verbose_name='پرداخت شده', null=True)

    def the_difference(self):
        return self.amount_payable - self.amount_paid

    def get_username(self):
        """Return the username for this User. this function overwrite from same name function in class AbstractBaseUser"""
        return self.student_number

    def clean(self):
        username = self.student_number
        normalized_username = self.normalize_username(username)
        self.username = normalized_username

    def save(self, *args, **kwargs):
        if self.start_date_of_study:
            self.deadline_date_of_study = self.start_date_of_study + relativedelta(years=6)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'دانشجو'
        verbose_name_plural = 'دانشجویان'


class EvaluationByStudent(models.Model):
    for_student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='دانشجو', null=True)
    presentation = models.ForeignKey('service_module.Presentation', on_delete=models.CASCADE, verbose_name='ارائه مرتبط')
    teaching_skills = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name='مهارت تدریس')
    punctuality = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name='وقت شناسی')
    respectful_behavior = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name='رفتار محترمانه')

    def __str__(self):
        return f'{self.for_student} - {self.presentation.teacher} - {self.presentation.lesson}'

    class Meta:
        verbose_name = 'ارزیابی استاد'
        verbose_name_plural = 'ارزیابی اساتید'


class Marks(models.Model):
    for_student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='دانشجو', null=True)
    for_semester = models.ForeignKey('service_module.Semester', on_delete=models.CASCADE, verbose_name='برای نیمسال', null=True)
    presentation = models.ForeignKey('service_module.Presentation', on_delete=models.CASCADE, verbose_name='درس ارائه شده')
    mark = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(20)], verbose_name='نمره', null=True)

    class Meta:
        verbose_name = 'نمره'
        verbose_name_plural = 'نمرات'


class SemesterGPA(models.Model):
    for_student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='دانشجو', null=True)
    semester = models.ForeignKey('service_module.Semester', on_delete=models.CASCADE, verbose_name='نیمسال', null=True)
    semester_GPA = models.FloatField(validators=[MinValueValidator(0)], verbose_name='معدل نیمسال')
    total_GPA = models.FloatField(validators=[MinValueValidator(0)], verbose_name='معدل تاکنون')
    mark = models.ManyToManyField(Marks, verbose_name='دروس نیمسال', blank=True)
    obtained_units = models.FloatField(verbose_name='واحد های اخذ شده نیمسال')
    passed_units = models.FloatField(verbose_name='واحد های گذرانده نیمسال')
    rejected_units = models.FloatField(verbose_name='واحد های رد شده نیمسال')

    class Meta:
        verbose_name = 'معدل'
        verbose_name_plural = 'معدل ها'


class StudentGradeAppeal(models.Model):
    for_student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='دانشجو')
    semester = models.ForeignKey('service_module.Semester', on_delete=models.CASCADE, verbose_name='نیمسال', null=True)
    mark = models.ForeignKey(Marks, on_delete=models.CASCADE, verbose_name='نمره مرتبط', blank=True, null=True)
    appel_text = models.TextField(verbose_name='متن اعتراض')
    response_teacher = models.TextField(verbose_name='پاسخ استاد')
    is_response = models.BooleanField(default=False, verbose_name='پاسخ داده شده / نشده')

    class Meta:
        verbose_name = 'اعتراض به نمره'
        verbose_name_plural = 'اعتراض به نمرات'
