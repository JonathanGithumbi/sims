from pyexpat.errors import messages
from unicodedata import numeric
from urllib.request import proxy_bypass
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from requests import delete
from . import forms
from user_account.models import CustomUser
from student.models import Student
from financial_account.models import FinancialAccount
from info.models import FeesStructure
from django.contrib.auth.models import BaseUserManager
import datetime 
from datetime import datetime,timedelta
from info.models import AcademicCalendar
import pytz
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import io
from django.http import FileResponse
from financial_account.models import CurrentBalance
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from .utils import render_to_pdf

@login_required
def admin_dashboard(request):
    """This view lands the user on  the administration dashboard"""
    number_of_students = Student.objects.all().count()
    records = CurrentBalance.objects.filter(current_balance__lt = 0).count()
    lunch_subscribers = Student.objects.filter(hot_lunch=True).count()
    transport_subscribers = Student.objects.filter(transport=True).count()
    context ={
        'number_of_students':number_of_students,
        'records':records ,# Studentts with fees arrears
        'lunch_subscribers':lunch_subscribers,
        'transport_subscribers':transport_subscribers
    }
    return render(request,'administrator/admin_dashboard.html', {'context':context})

def date_range(start,end):
    """This view returns a list of datetime instances  of days between 'start' day and 'end' day """
    """It is used in get_term() to retrieve the term number """
    delta = end-start
    days = [start + timedelta(days=i) for i in range(delta.days+1)]
    return days

def get_term(date):
    """This method returns the term number (int) given the date """
    """Uses date_range() to retrieve the list of days in a term"""
    """It works as long as the time on the datetime instances of AcademicCaalendar are set to 00:00 (midnight)"""
    calendar = AcademicCalendar.objects.get(year=date.year)
    term_1_start_date = calendar.term_1_start_date
    term_1_end_date = calendar.term_1_end_date
    term_2_start_date =calendar.term_2_start_date
    term_2_end_date = calendar.term_2_end_date
    term_3_start_date = calendar.term_3_start_date
    term_3_end_date = calendar.term_3_end_date

    term_1_days = date_range(term_1_start_date,term_1_end_date)
    term_2_days = date_range(term_2_start_date,term_2_end_date)
    term_3_days = date_range(term_3_start_date,term_3_end_date)

    if date in term_1_days:
        return 1
    if date in term_2_days:
        return 2
    if date in term_3_days:
        return 3

def get_term_amount(date,grade,lunch,transport,transport_fee):#Lunch and transport are optionals 
    """This function retrieves the fees due for a given term, provided the current date"""
    """this date is a datetime.now() instance from when the student is being regisetred"""
    """it returns the amount due for a given term ther amount will be negative to indicate amout is due"""
    """This method is used only during student registration, a separate function get_term_amount_continous() calculates the amount for continuing students """
    #date is a datetime instance
    year = date.year#This is the date the student joined
    term = get_term(date)
    fee = FeesStructure.objects.get(year=2022,term=term,grade=grade)

    amount = fee.tuition_fee + fee.computer_lessons + fee.diary_and_report_book + fee.interview_fee + fee.admission_fee
    if lunch and not transport:
        amount  = amount+ fee.hot_lunch
    if transport and not lunch:
        amount = amount + transport_fee
    if transport and lunch :
        amount = amount + transport_fee + fee.hot_lunch
        
    return -abs(amount)

def get_standard_datetime():
    """This method returns a standard datetime instance that i can use in get_term_amount() to retrieve the amount due for that terms"""
    #Construct the datetime instance of today (when the student is registered)
    today = datetime.now(tz=pytz.UTC)
    year = today.year
    month = today.month
    day = today.day
    date = datetime(year,month,day)
    #Making the datetime 'timezone aware', so that it can be used by get_term()
    date = date.replace(tzinfo=pytz.UTC)
    return date

@login_required
def register_student(request):
    """This function registers a student which is then associated with a financial account"""
    if request.method == 'GET':
        form = forms.StudentRegistrationForm()
        return render(request,'administrator/student_registration_page.html',{'form':form})
    if request.method =='POST':
        form = forms.StudentRegistrationForm(request.POST)
        if form.is_valid():
            # 1. Create the student
            student = Student()
            student.first_name = form.cleaned_data['first_name']
            student.middle_name = form.cleaned_data['middle_name']
            student.last_name = form.cleaned_data['last_name']
            student.date_of_birth = form.cleaned_data['date_of_birth']
            student.gender = form.cleaned_data['gender']
            student.grade_admitted_to = form.cleaned_data['grade_admitted_to']
            student.current_grade = form.cleaned_data['grade_admitted_to']
            student.primary_contact_name = form.cleaned_data['primary_contact_name']
            student.primary_contact_phone_number = form.cleaned_data['primary_contact_phone_number']
            student.secondary_contact_name = form.cleaned_data['secondary_contact_name']
            student.secondary_contact_phone_number = form.cleaned_data['secondary_contact_phone_number']
            student.hot_lunch = form.cleaned_data['hot_lunch']
            student.transport = form.cleaned_data['transport']
            student.transport_fee = form.cleaned_data['transport_fee']
            student.save()

            # 3. Create the financial account
                    # - We need to know which term and year we are now given the date
                    # - calculate the core fees items without optioinals, if we have optionals, add them
                    # - create a financial account and Credit that amount to the student financial account
            transaction = FinancialAccount()
            transaction.student = student

            #optionals
            lunch = form.cleaned_data['hot_lunch']
            transport = form.cleaned_data['transport']
            transport_fee = form.cleaned_data['transport_fee']
            date = get_standard_datetime()

            #Crediting the student the term's fees "+(-amount)"
            #Transaction Amount. How Much is the student going to get charged for this term
            transaction.amount = get_term_amount(date,student.grade_admitted_to,lunch,transport,transport_fee)#How much is due for the current term
            transaction.description = "term's fees" 
            transaction.arrears = get_term_amount(date,student.grade_admitted_to,lunch,transport,transport_fee)
            transaction.transaction_type = 'credit'
            transaction.for_term = get_term(date)
            transaction.for_year = date.year
            transaction.save()
            messages.add_message(request,messages.SUCCESS,"Student Registered Successfully")
            return HttpResponseRedirect(reverse('student_profile', args=[student.id]))
        else:
            return render(request,'administrator/student_registration_page.html',{'form':form})
@login_required
def student_profile(request,id):
    """this function displays the student's information including financial history"""
    """Gives access to  update, delete and downloading and printing of financial documents"""
    student = Student.objects.get(pk=id)
    return render(request, 'administrator/student_profile_page.html',{'student':student})
@login_required
def search_student(request):
    """Searches for a given student given the first name and grade """
    if request.method == 'GET':
        form = forms.SearchStudentForm()
        return render(request, 'administrator/search_student_page.html',{'form':form})
    if request.method == 'POST':
        form = forms.SearchStudentForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            
            grade = form.cleaned_data['grade']

            #this feature allows for getting all the students from a certain grade
            if grade and not first_name :
                students = Student.objects.filter(current_grade=grade)
                return render(request, 'administrator/search_student_page.html',{'students':students,'form':form})
            if grade and first_name:
                students = Student.objects.filter(current_grade=grade).filter(user__first_name__iexact = first_name)
                return render(request, 'administrator/search_student_page.html',{'students':students,'form':form})
            
        else:
            return render(request, 'administrator/search_student_page.html',{'form':form})
@login_required       
def update_student(request,id):
    """Updates student details """
    """updates fees structure when you update fees structure attributes"""
    student = Student.objects.get(pk=id)
    data = {
            'student_type': student.student_type,
            'first_name' : student.first_name,
            'middle_name' : student.middle_name,
            'last_name' : student.last_name, 
            'gender' : student.gender,
            'date_of_birth' : student.date_of_birth,
            'grade_admitted_to' :  student.grade_admitted_to,
            'primary_contact_name' : student.primary_contact_name,
            'primary_contact_phone_number' : student.primary_contact_phone_number,
            'secondary_contact_name' : student.secondary_contact_name,
            'secondary_contact_phone_number' : student.secondary_contact_phone_number,
            'hot_lunch' : student.hot_lunch,
            'charge_admission_fee':student.charge_admission_fee,
            'transport' : student.transport,
            'transport_fee':student.transport_fee
        }
    if request.method == 'GET':
        form = forms.StudentRegistrationForm(data)
        return render(request, 'administrator/student_update_page.html',{'form':form,'student':student})
    if request.method == 'POST':
        form = forms.StudentRegistrationForm(request.POST,initial=data)
        if form.is_valid():
            if form.has_changed():
                changed_data = form.changed_data
                #these are the changed fees structure attributes which will alter the amount credited for that term which will in turn alter the transaction history of the student 
                if 'grade_admitted_to' in changed_data or 'hot_lunch' in changed_data or 'transport' in changed_data or 'transport_fee' in changed_data or 'charge_admission_fee' in changed_data:
                    date = get_standard_datetime()
                    new_grade = form.cleaned_data['grade_admitted_to']
                    lunch = form.cleaned_data['hot_lunch']
                    transport = form.cleaned_data['transport']
                    transport_fee = form.cleaned_data['transport_fee']
                    if transport == False:
                        transport_fee = 0                                             
                    charge_admission_fee = form.cleaned_data['charge_admission_fee']
                    student_type = form.cleaned_data['student_type']
                    new_amount = get_term_amount(date,new_grade,lunch,transport,charge_admission_fee,transport_fee,student_type)
                    #retrieve the term's fees transaction
                    transaction =student.financialaccount_set.get(transaction_type='credit',description="term's fees",for_year=date.year, for_term=get_term(date))
                    transaction.amount = new_amount
                    transaction.arrears = new_amount
                    transaction.save()
                student.first_name = form.cleaned_data['first_name']
                student.middle_name = form.cleaned_data['middle_name']
                student.last_name = form.cleaned_data['last_name']
                student.date_of_birth = form.cleaned_data['date_of_birth']
                student.gender = form.cleaned_data['gender']
                student.grade_admitted_to = form.cleaned_data['grade_admitted_to']
                student.primary_contact_name = form.cleaned_data['primary_contact_name']
                student.primary_contact_phone_number = form.cleaned_data['primary_contact_phone_number']
                student.secondary_contact_name = form.cleaned_data['secondary_contact_name']
                student.secondary_contact_phone_number = form.cleaned_data['secondary_contact_phone_number']
                student.hot_lunch = form.cleaned_data['hot_lunch']
                student.transport = form.cleaned_data['transport']
                student.transport_fee = form.cleaned_data['transport_fee']
                student.charge_admission_fee = form.cleaned_data['charge_admission_fee']
                student.save()
                messages.add_message(request,messages.SUCCESS,"Student infomation updated ")
                return redirect(reverse('student_profile', args=[student.id]))
            else:
                messages.add_message(request,messages.SUCCESS,"No information Altered!")
                return redirect(reverse('student_profile', args=[student.id]))
        else:
            return render(request, 'administrator/student_update_page.html',{'form':form})
@login_required
def delete_student(request, id):
    """Deletes a user which deletes the student which deletes the account"""
    user = Student.objects.get(pk=id)
    user.delete()
    messages.add_message(request,messages.SUCCESS,'Student Deleted Successfully')
    return redirect(reverse('administrator_dashboard'))
@login_required
def make_payment(request,id):
    """Making debit transactions"""
    """This is used for debiting amounts to a student's account"""
    student = Student.objects.get(pk=id)
    if request.method == 'GET':
        form = forms.MakePaymentForm()
        return render(request, 'administrator/make_payment_page.html',{'form':form,'student':student})
    if request.method == 'POST':
        form = forms.MakePaymentForm(request.POST)
        if form.is_valid():
            prev_transaction = student.financialaccount_set.order_by('-date_of_payment').first()
            print(prev_transaction.amount)
            prev_arrears = prev_transaction.arrears
            arrears = prev_arrears + form.cleaned_data['amount']
            transaction = student.financialaccount_set.create(
            transaction_type = 'debit',
            amount = form.cleaned_data['amount'],
            arrears = arrears,
            student = student ,
            )
            transaction.save()
            messages.add_message(request,messages.SUCCESS,'Payment made successfully')
            return redirect(reverse('student_profile',args=[student.id]))
        else:
            return render(request,'administrator/make_payment_page.html',{'form':form,'student':student})
@login_required
def transaction_details(request, id ):
    """displays transaction details and allows you to print/download receipt for a payment """
    transaction = FinancialAccount.objects.get(pk=id)
    return render(request,'administrator/transaction_details.html',{'transaction':transaction})
@login_required
def download_statement(request, id):
    student= Student.objects.get(pk=id)
    transactions = FinancialAccount.objects.filter(student=student)
    context = {'transactions':transactions}
    template_name = 'administrator/transaction_history_report.html'
    pdf = render_to_pdf(template_name,context)
    return HttpResponse(pdf, content_type='application/pdf')
@login_required
def download_receipt(request, id):
    transaction = FinancialAccount.objects.get(id=id)
    context = {'transaction':transaction}
    template_name = 'administrator/transaction_details.html'
    pdf = render_to_pdf(template_name,context)
    return HttpResponse(pdf, content_type='application/pdf')
@login_required
def reports(request):
    """displays options to display and print reports {'students with high arrears','students taking hot lunch this term','students taking transport this year'}"""
    return render(request, 'administrator/reports.html')
@login_required
def search_fees_structure(request):
    """Displays the current fees structure for a give year,term"""
    """Fees structures are grade-wise"""
    if request.method == 'GET':
        form = forms.FeesStructureSearchForm()
        return render(request, 'administrator/search_fees_structure_page.html',{'form':form})
    if request.method == 'POST':
        form = forms.FeesStructureSearchForm(request.POST)
        if form.is_valid():
            fees_struc = FeesStructure.objects.filter(
                year = form.cleaned_data['year'],
                term = form.cleaned_data['term'],
                grade = form.cleaned_data['grade']
            )
            return render(request,'administrator/search_fees_structure_page.html',{'fees_struc':fees_struc,'form':form})
        else:
            return render(request, 'administrator/search_fees_structure_page.html')
@login_required
def update_fees_structure(request,id):
    fees_struc = FeesStructure.objects.get(pk=id)
    if request.method ==  'GET':
        data = {
            'year' : fees_struc.year,
            'term': fees_struc.term,
            'grade':fees_struc.grade,
            'admission':fees_struc.admission,
            'diary_and_report_book':fees_struc.diary_and_report_book,
            'interview_fee':fees_struc.interview_fee,
            'tuition_fee':fees_struc.tuition_fee,
            'computer_lessons':fees_struc.computer_lessons,
            'hot_lunch':fees_struc.hot_lunch,

        }
        form = forms.FeesStructureUpdateForm(data=data)
        return render(request, 'administrator/fees_structure_update_page.html',{'form':form})
    if request.method == 'POST':
        form = forms.FeesStructureUpdateForm(request.POST)
        if form.is_valid():
            fees_struc.year = form.cleaned_data['year']
            fees_struc.term = form.cleaned_data['term']
            fees_struc.grade = form.cleaned_data['grade']
            fees_struc.admission = form.cleaned_data['admission']
            fees_struc.diary_and_report_book = form.cleaned_data['diary_and_report_book']
            fees_struc.interview_fee = form.cleaned_data['interview_fee']
            fees_struc.tuition_fee = form.cleaned_data['tuition_fee']
            fees_struc.computer_lessons = form.cleaned_data['computer_lessons']
            fees_struc.hot_lunch = form.cleaned_data['hot_lunch']
            fees_struc.save()
            form = forms.FeesStructureSearchForm()
            return render(request, 'administrator/search_fees_structure_page.html',{'form':form,'fees_struc':fees_struc})
@login_required
def generate_fees_arrears_report(request):
    # get a list of all the students whose arrears is less than 0
    # make sure to get the latest transaction for a given student
    records = CurrentBalance.objects.filter(current_balance__lt = 0).order_by('-current_balance')
    context = {'records':records}
    template_name = 'administrator/fees_arrears_report.html'
    pdf = render_to_pdf(template_name,context)
    return HttpResponse(pdf, content_type='application/pdf')
@login_required
def generate_lunch_subscribers_report(request):
    students = Student.objects.filter(hot_lunch=True)
    context = {'students':students}
    template_name = 'administrator/lunch_report.html'
    pdf = render_to_pdf(template_name,context)
    return HttpResponse(pdf, content_type='application/pdf')
@login_required
def generate_transport_subscribers_report(request):
    students = Student.objects.filter(transport=True)
    context = {'students':students}
    template_name = 'administrator/transport_report.html'
    pdf = render_to_pdf(template_name,context)
    return HttpResponse(pdf, content_type='application/pdf')
@login_required
def generate_fees_structure_report(request):
    fees_structures = FeesStructure.objects.all()
    pass

def migrate_records(request):
    pass

def get_all_students(request):
    students = Student.objects.all()
    return render(request, 'administrator/all_students.html',{'students':students})

def charge_student(request,id):
    if request.method == 'GET':
        form = forms.ChargeStudentForm()
        return render(request,'administrator/charge_student.html',{'form':form,'id':id})
    if request.method == 'POST':
        pass