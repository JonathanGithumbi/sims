# Generated by Django 3.2.9 on 2022-06-15 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_alter_student_charge_admission_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='charge_admission_fee',
        ),
        migrations.RemoveField(
            model_name='student',
            name='student_type',
        ),
    ]
