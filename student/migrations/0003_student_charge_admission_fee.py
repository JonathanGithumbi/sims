# Generated by Django 3.2.9 on 2022-05-30 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20220527_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='charge_admission_fee',
            field=models.BooleanField(default=True),
        ),
    ]