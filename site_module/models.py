from django.db import models
from multiselectfield import MultiSelectField
from staff_module.models import Staff
from student_module.models import Student
from teacher_module.models import Teacher


# Create your models here.


class ContactMessages(models.Model):
    from_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, verbose_name='دانشجو')
    from_operator = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='اپراتور')
    message = models.TextField(verbose_name='متن پیام')
    is_response = models.BooleanField(default=False, verbose_name='پاسخ داده شده؟')
    create_date = models.DateTimeField(auto_now=True, verbose_name='زمان ارسال')

    class Meta:
        verbose_name = 'پیام های تیکت'
        verbose_name_plural = 'پیام های تیکت ها'


class ContactRequest(models.Model):
    from_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, verbose_name='برای دانشجو')
    from_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, verbose_name='برای استاد')
    from_staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='برای کارمند')
    # from_operator = models.ForeignKey(Staff, on_delete=models.CASCADE)
    subject = models.TextField(verbose_name='موضوع')
    contact_message = models.ManyToManyField(ContactMessages, blank=True, verbose_name='پیام ها')
    is_closed = models.BooleanField(default=False, verbose_name='بسته شده / بسته نشده')
    create_date = models.DateTimeField(auto_now=True, verbose_name='زمان ارسال')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'


# use django-multiselectfield package for field 'for_group'
class Faq(models.Model):
    QUESTIONS_CHOICES = (
        ('student', 'دانشجو'),
        ('teacher', 'استاد'),
        ('staff', 'کارمند'),
    )

    title = models.CharField(max_length=600, verbose_name='عنوان سوالات')
    description = models.TextField(verbose_name='توضیحات')
    priority = models.IntegerField(unique=True, verbose_name='ترتیب')
    for_group = MultiSelectField(choices=QUESTIONS_CHOICES, max_choices=100, max_length=100, verbose_name='برای گروه...')

    class Meta:
        verbose_name = 'سوال کاربر'
        verbose_name_plural = 'سوالات کاربر'


class IndexMessages(models.Model):
    QUESTIONS_CHOICES = (
        ('student', 'دانشجو'),
        ('teacher', 'استاد'),
        ('staff', 'کارمند'),
    )

    title = models.CharField(max_length=700, verbose_name='عنوان پیام')
    content = models.TextField(verbose_name='محتوای پیام')
    priority = models.IntegerField(verbose_name='اولویت')
    for_group = MultiSelectField(choices=QUESTIONS_CHOICES, max_choices=100, max_length=100, verbose_name='برای گروه...')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'اطلاعیه'
        verbose_name_plural = 'اطلاعیه ها'
