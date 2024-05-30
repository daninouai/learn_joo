import uuid
from django.db import models
from student_module.models import Student
from teacher_module.models import Teacher
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.class_formation_times import ClassFormationTime


# Create your models here.


class Semester(models.Model):
    semester_number = models.IntegerField(verbose_name='شماره ترم', unique=True, null=True)
    is_main_semester = models.BooleanField(verbose_name='نیمسال جاری؟', default=False, null=True)
    select_unit_permission = models.BooleanField(verbose_name='مجوز انتخاب واحد', default=False)
    start_select_unit_time = models.DateTimeField(verbose_name='زمان شروع انتخاب واحد', null=True, blank=True)
    end_select_unit_time = models.DateTimeField(verbose_name='زمان پایان انتخاب واحد', null=True, blank=True)

    def __str__(self):
        return f'{self.semester_number}'

    class Meta:
        verbose_name = 'ترم'
        verbose_name_plural = 'ترم ها'


class Lesson(models.Model):
    class UnitsStatusType(models.TextChoices):
        HALF_UNITS = 'half_units', 'نیم واحد'
        SINGLE_UNITS = 'single_units', 'یک واحد'
        TWO_UNITS = 'two_units', 'دو واحد'
        THREE_UNITS = 'three_units', 'سه واحد'
        FOUR_UNITS = 'four_units', 'چهار واحد'
        FIVE_UNITS = 'five_units', 'پنج واحد'

    class LessonCourseType(models.TextChoices):
        FOUNDATION = 'foundation', 'پایه'
        PROFESSIONAL = 'professional', 'تخصصی'
        MAIN = 'main', 'اصلی'
        GENERAL = 'general', 'عمومی'

    class LessonType(models.TextChoices):
        PRACTICAL = 'practical', 'عملی'
        THEORETICAL = 'theoretical', 'نظری'
        PRACTICAL_THEORETICAL = 'practical_theoretical', 'نظری - عملی'

    lesson_name = models.CharField(max_length=300, verbose_name='نام درس')
    lesson_code = models.SmallIntegerField(verbose_name='کد درس')
    lesson_course = models.CharField(max_length=200, choices=LessonCourseType.choices, verbose_name='نوع درس', db_column='lesson_course_type_en', null=True)
    theoretical_unit = models.CharField(max_length=200, choices=UnitsStatusType.choices, null=True, blank=True, verbose_name='واحد نظری', db_column='theoretical_unit_en')
    practical_units = models.CharField(max_length=200, choices=UnitsStatusType.choices, null=True, blank=True, verbose_name='واحد عملی', db_column='practical_units_en')
    lesson_type = models.CharField(max_length=200, choices=LessonType.choices, verbose_name='نوع درس رشته', db_column='lesson_type_en')
    prerequisite_lesson = models.ManyToManyField('self', verbose_name='دروس پیشنیاز', blank=True)

    def __str__(self):
        return f'{self.lesson_code} - {self.lesson_name}'

    class Meta:
        verbose_name = 'درس'
        verbose_name_plural = 'درس ها'


class ExamTime(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان نمایشی')
    start_time = models.DateTimeField(verbose_name='زمان شروع آزمون')
    end_time = models.DateTimeField(verbose_name='زمان پایان آزمون')

    class Meta:
        verbose_name = 'زمانبندی آزمون'
        verbose_name_plural = 'زمانبندی آزمون ها'


class Presentation(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='نام استاد')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='نام درس')
    student = models.ManyToManyField(Student, verbose_name='دانشجویان', blank=True)
    capacity = models.IntegerField(verbose_name='ظرفیت', null=True, blank=True)
    for_semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name='ترم ارائه شده', null=True, blank=True)
    class_formation_time = models.CharField(max_length=200, choices=ClassFormationTime.choices, verbose_name='زمان تشکیل کلاس', null=True, blank=True, db_column='class_formation_time_en')
    exam_time = models.ForeignKey(ExamTime, on_delete=models.CASCADE, verbose_name='زمان امتحان', null=True, blank=True)

    def __str__(self):
        return f'{self.lesson.lesson_name} - {self.for_semester} - {self.teacher}'

    def remaining_capacity(self):
        return self.capacity - self.student.count()

    class Meta:
        verbose_name = 'درس ارائه شده'
        verbose_name_plural = 'دروس ارائه شده'


class EducationGroup(models.Model):
    name = models.CharField(max_length=300, verbose_name='نام گروه آموزشی')

    def __str__(self):
        return f'{self.name}'

    def get_show_name(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'گروه آموزشی'
        verbose_name_plural = 'گروه های آموزشی'


class Major(models.Model):
    class SectionType(models.TextChoices):
        CONTINUOUS_ASSOCIATE = 'continuous_associate', 'کاردانی پیوسته'
        DISCONTINUOUS_ASSOCIATE = 'discontinuous_associate', 'کاردانی نا پیوسته'
        BACHELORS_DEGREE = 'bachelors_degree', 'کارشناسی پیوسته'
        DISCONTINUOUS_BACHELORS_DEGREE = 'discontinuous_bachelors_degree', 'کارشناسی نا پیوسته'
        MASTERS = 'masters', 'کارشناسی ارشد'
        DOCTORATE = 'doctorate', 'دکترا'

    major_name = models.CharField(max_length=300, verbose_name='نام رشته')
    educational_group = models.ForeignKey(EducationGroup, on_delete=models.CASCADE, verbose_name='گروه آموزشی')
    section = models.CharField(max_length=300, choices=SectionType.choices, db_column='section_en', verbose_name='مقطع رشته')

    def __str__(self):
        return f'{self.major_name} - {self.educational_group} - {self.get_section_display()}'

    def get_show_name(self):
        return f'{self.major_name} - {self.get_section_display()}'

    class Meta:
        verbose_name = 'رشته تحصیلی'
        verbose_name_plural = 'رشته های تحصیلی'


class Requests(models.Model):
    class RequestType(models.TextChoices):
        PERMISSION_SELECT_UNIT = 'permission_select_unit', 'مجوز انتخاب واحد'
        REQUEST_FOR_FACILITIES = 'request_for_facilities', 'درخواست تسهیلات'

    class StatusType(models.TextChoices):
        CONFIRMED = 'confirmed', 'تایید شده'
        REJECTED = 'rejected', 'رد شده'
        PENDING = 'pending', 'در حال بررسی'

    request_number = models.UUIDField(unique=True, default=uuid.uuid4, verbose_name='شماره درخواست')
    request_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    request_type = models.CharField(max_length=300, choices=RequestType.choices, verbose_name='نوع درخواست', db_column='request_type_en')
    for_semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name='نیمسال موثر', null=True)
    for_student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='برای دانشجو')
    status = models.CharField(max_length=300, choices=StatusType.choices, verbose_name='وضعیت', null=True, db_column='status_en')
    request_text = models.TextField(verbose_name='متن درخواست', null=True, blank=True)

    class Meta:
        verbose_name = 'درخواست'
        verbose_name_plural = 'درخواست ها'


class Bill(models.Model):
    class BillType(models.TextChoices):
        INSURANCE = 'insurance', 'بیمه'
        DORMITORY_TUITION = 'dormitory_tuition', 'شهریه خوابگاه'
        FIXED_TUITION = 'fixed_tuition', 'شهریه ثابت'
        VARIABLE_TUITION = 'variable_tuition', 'شهریه متغیر'
        STUDENT_WELFARE_FUND_FACILITIES = 'student_welfare_fund_facilities', 'تسهیلات صندوق رفاه دانشجویی'

    for_student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='دانشجو')
    for_semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name='نیمسال موثر', null=True)
    amount = models.SmallIntegerField(verbose_name='مبلغ')
    type = models.CharField(max_length=300, choices=BillType.choices, verbose_name='نوع صورت حساب', db_column='type_en')
    date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ صدور')
    bill_id = models.UUIDField(unique=True, default=uuid.uuid4, verbose_name='شناسه صورت حساب')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده/نشده')

    class Meta:
        verbose_name = 'صورت حساب'
        verbose_name_plural = 'صورت حساب ها'


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        CONFIRMED = 'confirmed', 'تایید شده'
        PENDING = 'pending', 'در حال بررسی'
        REJECTED = 'rejected', 'رد شده'

    for_semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name='برای نیمسال', null=True)
    for_student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='دانشجو')
    amount = models.SmallIntegerField(verbose_name='مبلغ پرداخت شده')
    date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پرداخت')
    payment_id = models.UUIDField(unique=True, default=uuid.uuid4, verbose_name='شناسه پرداخت')
    status = models.CharField(max_length=300, choices=PaymentStatus.choices, verbose_name='وضعیت', null=True, db_column='status_en')
    for_bill = models.ForeignKey(Bill, on_delete=models.CASCADE, verbose_name='برای صورت حساب', null=True, blank=True)

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'


class FixedTuition(models.Model):
    class SectionType(models.TextChoices):
        CONTINUOUS_ASSOCIATE = 'continuous_associate', 'کاردانی پیوسته'
        DISCONTINUOUS_ASSOCIATE = 'discontinuous_associate', 'کاردانی نا پیوسته'
        BACHELORS_DEGREE = 'bachelors_degree', 'کارشناسی پیوسته'
        DISCONTINUOUS_BACHELORS_DEGREE = 'discontinuous_bachelors_degree', 'کارشناسی نا پیوسته'
        MASTERS = 'masters', 'کارشناسی ارشد'
        DOCTORATE = 'doctorate', 'دکترا'

    entrance_semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name='برای ورودی نیمسال', null=True)
    educational_group = models.ForeignKey(EducationGroup, on_delete=models.CASCADE, verbose_name='گروه آموزشی')
    section = models.CharField(max_length=300, choices=SectionType.choices, db_column='section_en', verbose_name='مقطع رشته')
    cost = models.SmallIntegerField(verbose_name='هزینه شهریه ثابت')

    class Meta:
        verbose_name = 'شهریه ثابت'
        verbose_name_plural = 'شهریه های ثابت'


class VariableTuition(models.Model):
    class SectionType(models.TextChoices):
        CONTINUOUS_ASSOCIATE = 'continuous_associate', 'کاردانی پیوسته'
        DISCONTINUOUS_ASSOCIATE = 'discontinuous_associate', 'کاردانی نا پیوسته'
        BACHELORS_DEGREE = 'bachelors_degree', 'کارشناسی پیوسته'
        DISCONTINUOUS_BACHELORS_DEGREE = 'discontinuous_bachelors_degree', 'کارشناسی نا پیوسته'
        MASTERS = 'masters', 'کارشناسی ارشد'
        DOCTORATE = 'doctorate', 'دکترا'

    for_semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name='برای نیمسال', null=True)
    educational_group = models.ForeignKey(EducationGroup, on_delete=models.CASCADE, verbose_name='گروه آموزشی')
    section = models.CharField(max_length=300, choices=SectionType.choices, db_column='section_en', verbose_name='مقطع رشته')
    one_theoretical_unit = models.SmallIntegerField(verbose_name='میزان شهریه برای یک واحد نظری')
    one_practical_unit = models.SmallIntegerField(verbose_name='میزان شهریه برای یک واحد عملی')

    class Meta:
        verbose_name = 'شهریه متغیر'
        verbose_name_plural = 'شهریه های متغیر'