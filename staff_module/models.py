from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from account_module.models import User


# Create your models here.

class Staff(AbstractBaseUser):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')

    class ActivityStatusType(models.TextChoices):
        ACTIVE = 'active', 'فعال'
        INACTIVE = 'inactive', 'غیر فعال'

    class TypeOfEmployee(models.TextChoices):
        OFFICIAL = 'official', 'رسمی'
        CONTRACTUAL = 'contractual', 'قراردادی'

    personnel_code = models.CharField(max_length=200, unique=True, verbose_name='کد پرسنلی')
    activity_status = models.CharField(max_length=200, choices=ActivityStatusType.choices, verbose_name='وضعیت فعالیت', db_column='activity_status_en')
    start_date_of_working = models.DateField(verbose_name='تاریخ شروع به کار')
    type_of_employment = models.CharField(max_length=200, choices=TypeOfEmployee.choices, verbose_name='وضعیت قرارداد', db_column='type_of_employment_en')

    def get_username(self):
        """Return the username for this User. this function overwrite from same name function in class AbstractBaseUser"""
        return self.personnel_code

    def clean(self):
        username = self.personnel_code
        normalized_username = self.normalize_username(username)
        self.username = normalized_username

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمندان'
