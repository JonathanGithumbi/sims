# Generated by Django 3.2.9 on 2022-05-26 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('grade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('term_1_start_date', models.DateTimeField()),
                ('term_1_mid_term_break_start', models.DateTimeField()),
                ('term_1_mid_term_break_end', models.DateTimeField()),
                ('term_1_end_date', models.DateTimeField()),
                ('term_2_start_date', models.DateTimeField()),
                ('term_2_mid_term_break_start', models.DateTimeField()),
                ('term_2_mid_term_break_end', models.DateTimeField()),
                ('term_2_end_date', models.DateTimeField()),
                ('term_3_start_date', models.DateTimeField()),
                ('term_3_mid_term_break_start', models.DateTimeField()),
                ('term_3_mid_term_break_end', models.DateTimeField()),
                ('term_3_end_date', models.DateTimeField()),
                ('kcpe_start_date', models.DateTimeField()),
                ('kcpe_end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='FeesStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('term', models.IntegerField()),
                ('admission', models.IntegerField()),
                ('diary_and_report_book', models.IntegerField()),
                ('interview_fee', models.IntegerField(default=300)),
                ('tuition_fee', models.IntegerField()),
                ('computer_lessons', models.IntegerField(default=1000)),
                ('hot_lunch', models.IntegerField()),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade.grade')),
            ],
        ),
    ]