# Generated by Django 3.2.9 on 2022-06-04 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_auto_20220527_1426'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feesstructure',
            old_name='admission',
            new_name='admission_fee',
        ),
    ]
