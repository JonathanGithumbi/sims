# Generated by Django 3.2.9 on 2022-05-27 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academiccalendar',
            name='kcpe_end_date',
        ),
        migrations.RemoveField(
            model_name='academiccalendar',
            name='kcpe_start_date',
        ),
        migrations.RemoveField(
            model_name='academiccalendar',
            name='term_1_mid_term_break_end',
        ),
        migrations.RemoveField(
            model_name='academiccalendar',
            name='term_1_mid_term_break_start',
        ),
        migrations.RemoveField(
            model_name='academiccalendar',
            name='term_2_mid_term_break_end',
        ),
        migrations.RemoveField(
            model_name='academiccalendar',
            name='term_2_mid_term_break_start',
        ),
        migrations.RemoveField(
            model_name='academiccalendar',
            name='term_3_mid_term_break_end',
        ),
        migrations.RemoveField(
            model_name='academiccalendar',
            name='term_3_mid_term_break_start',
        ),
    ]