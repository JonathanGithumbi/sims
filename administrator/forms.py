from email.policy import default
from logging import PlaceHolder
from random import choices
from django import forms
from grade.models import Grade
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from django.core import validators
class StudentRegistrationForm(forms.Form):
    
    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female')
    )
    first_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    middle_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class':'w3-select w3-border w3-round-small'}))
    date_of_birth = forms.DateField(widget=forms.widgets.DateInput(attrs={'class':'w3-input w3-border w3-round-small','type':'date'}), input_formats=['%Y-%m-%d'])
    grade_admitted_to = forms.ModelChoiceField(queryset=Grade.objects.all(), widget=forms.Select(attrs={'class':'w3-input w3-border w3-round-small'}))
    primary_contact_name = forms.CharField( max_length=30,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    primary_contact_phone_number = forms.CharField( max_length=30,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    secondary_contact_name = forms.CharField( max_length=30, required=False,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    secondary_contact_phone_number = forms.CharField( max_length=30,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    hot_lunch = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w3-check w3-border w3-round-small'}))
    transport = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w3-check w3-border w3-round-small'}))
    transport_fee = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}), validators=[validators.MinValueValidator(limit_value=3000,message="Minimum Amount is 3000ksh !")])


class SearchStudentForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    grade =  forms.ModelChoiceField(queryset=Grade.objects.all(), widget=forms.Select(attrs={'class':'w3-input w3-border w3-round-small'}))



class MakePaymentForm(forms.Form):
    TERM_CHOICES = [
        ('1','1'),
        ('2','2'),
        ('3','3')
    ]
    YEAR_CHOICES = [
        ('2022','2022'),
        ('2021','2021'),
        ('2020','2020')
    ]
    for_term = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    for_year = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    amount = forms.DecimalField(max_digits=8,decimal_places=2, widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    # Transaction number for  API call to paybill/bank acc, for confirmation of transaction status
    #transaction_number = forms.IntegerField()

class FeesStructureSearchForm(forms.Form):
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small','placeholder':'YYYY'}))
    term = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small','placeholder':'1 ,2 ,3'}))
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), widget=forms.Select(attrs={'class':'w3-input w3-border w3-round-small'}))

class FeesStructureUpdateForm(forms.Form):
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small','placeholder':'YYYY'}))
    term = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small','placeholder':'1, 2, 3'}))
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), widget=forms.Select(attrs={'class':'w3-input w3-border w3-round-small'}))
    admission = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    diary_and_report_book = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    interview_fee = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    tuition_fee = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    computer_lessons = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    hot_lunch = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}))


class ChargeStudentForm(forms.Form):
    TERM_CHOICES = [
        ('1','1'),
        ('2','2'),
        ('3','3')
    ]
    YEAR_CHOICES = [
        ('2022','2022'),
        ('2021','2021'),
        ('2020','2020')
    ]
    amount = forms.DecimalField(max_digits=8,decimal_places=2, widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'})) 
    description = forms.CharField(max_length=100, required=False,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    for_term = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    for_year = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round-small'}))
    

