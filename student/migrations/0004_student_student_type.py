# Generated by Django 3.2.9 on 2022-05-31 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_student_charge_admission_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_type',
            field=models.CharField(default='continuing', max_length=20),
        ),
    ]
