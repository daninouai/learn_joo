# Generated by Django 4.1.6 on 2024-05-07 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('personnel_code', models.CharField(max_length=200, unique=True, verbose_name='کد پرسنلی')),
                ('activity_status', models.CharField(choices=[('active', 'فعال'), ('inactive', 'غیر فعال')], db_column='activity_status_en', max_length=200, verbose_name='وضعیت فعالیت')),
                ('start_date_of_working', models.DateField(verbose_name='تاریخ شروع به کار')),
                ('type_of_employment', models.CharField(choices=[('official', 'رسمی'), ('contractual', 'قراردادی')], db_column='type_of_employment_en', max_length=200, verbose_name='وضعیت قرارداد')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'کارمند',
                'verbose_name_plural': 'کارمندان',
            },
        ),
    ]
