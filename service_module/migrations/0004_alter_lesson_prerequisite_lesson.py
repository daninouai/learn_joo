# Generated by Django 4.1.6 on 2024-05-14 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_module', '0003_lesson_prerequisite_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='prerequisite_lesson',
            field=models.ManyToManyField(blank=True, to='service_module.lesson', verbose_name='دروس پیشنیاز'),
        ),
    ]