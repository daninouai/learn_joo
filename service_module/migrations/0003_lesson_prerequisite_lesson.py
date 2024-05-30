# Generated by Django 4.1.6 on 2024-05-14 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_module', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='prerequisite_lesson',
            field=models.ManyToManyField(blank=True, related_name='prerequisite_lesson', to='service_module.lesson', verbose_name='دروس پیشنیاز'),
        ),
    ]
