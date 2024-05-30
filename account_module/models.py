from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class MaritalType(models.TextChoices):
        مجرد = 'مجرد', 'مجرد'
        متاهل = 'متاهل', 'متاهل'

    class GenderType(models.TextChoices):
        مرد = 'مرد', 'مرد'
        زن = 'زن', 'زن'

    class ReligionType(models.TextChoices):
        shia_muslim = 'مسلمان شیعه', 'مسلمان شیعه'
        sunni_muslim = 'مسلمان سنی', 'مسلمان سنی'
        christian = 'مسیحی', 'مسیحی'

    class MilitaryServiceStatus(models.TextChoices):
        exempt = 'معاف', 'معاف'
        education_pardon = 'معافیت تحصیلی', 'معافیت تحصیلی'
        served = 'خدمت کرده', 'خدمت کرده'

    latin_name = models.CharField(max_length=300, verbose_name='نام لاتین')
    latin_family_name = models.CharField(max_length=300, verbose_name='نام خانوادگی لاتین')
    father_name = models.CharField(max_length=300, verbose_name='نام پدر')
    national_code = models.SmallIntegerField(unique=True, verbose_name='کد ملی', null=True)
    certificate_number = models.SmallIntegerField(unique=True, verbose_name='شماره شناسنامه', null=True)
    birth_date = models.DateField(verbose_name='تاریخ تولد', null=True)
    image = models.ImageField(upload_to='images/user_images', verbose_name='تصویر کاربر', null=True)
    marital_status = models.CharField(max_length=200, choices=MaritalType.choices, verbose_name='تاهل', null=True)
    gender = models.CharField(max_length=200, choices=GenderType.choices, verbose_name='جنسیت', null=True)
    religion = models.CharField(max_length=200, choices=ReligionType.choices, verbose_name='دین', null=True)
    is_native = models.BooleanField(default=False, verbose_name='بومی / غیر بومی', null=True)
    place_of_issue = models.CharField(max_length=300, verbose_name='محل صدور', null=True)
    military_service_status = models.CharField(max_length=200, choices=MilitaryServiceStatus.choices, verbose_name='وضعیت خدمت', null=True)
    phone_number = models.CharField(max_length=300, verbose_name='شماره تلفن', null=True)

    def __str__(self):
        return str(f'{self.first_name} {self.last_name}')
