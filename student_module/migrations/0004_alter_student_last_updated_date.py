# Generated by Django 4.1.6 on 2024-05-07 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_module', '0003_alter_student_deadline_date_of_study'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='last_updated_date',
            field=models.DateField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
    ]