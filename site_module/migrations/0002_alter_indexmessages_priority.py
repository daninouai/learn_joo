# Generated by Django 4.1.6 on 2024-05-07 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexmessages',
            name='priority',
            field=models.IntegerField(verbose_name='اولویت'),
        ),
    ]
