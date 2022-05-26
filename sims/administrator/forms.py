from logging import PlaceHolder
from django import forms
from grade.models import Grade
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

class StudentRegistrationForm(forms.Form):
    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female')
    )
    first_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round'}))
    middle_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round'}))
    last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class':'w3-input w3-border w3-round'}))
    #image = forms.ImageField(required=False)
    email =forms.EmailField( widget=forms.EmailInput(attrs={'class':'w3-input w3-border w3-round'}))
    date_of_birth = forms.DateField(widget=forms.widgets.DateInput(attrs={'class':'w3-input w3-border w3-round','type':'date'}), input_formats=['%Y-%m-%d'])
    grade_admitted_to = forms.ModelChoiceField(queryset=Grade.objects.all(), widget=forms.Select(attrs={'class':'w3-input w3-border w3-round'}))
    primary_contact_name = forms.CharField( max_length=30,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round'}))
    primary_contact_phone_number = PhoneNumberField(widget=PhoneNumberInternationalFallbackWidget)
    secondary_contact_name = forms.CharField( max_length=30, required=False,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round'}))
    secondary_contact_phone_number = PhoneNumberField(widget=PhoneNumberInternationalFallbackWidget)
    hot_lunch = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w3-input w3-border w3-round'}))
    transport = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w3-input w3-border w3-round'}))
    transport_fee = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round'}))
class SearchStudentForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round'}))
    grade =  forms.ModelChoiceField(queryset=Grade.objects.all(), widget=forms.Select(attrs={'class':'w3-input w3-border w3-round'}))



class MakePaymentForm(forms.Form):
    """"""
    amount = forms.DecimalField(max_digits=8,decimal_places=2, widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round'}))
    # Transaction number for  API call to paybill/bank acc, for confirmation of transaction status
    #transaction_number = forms.IntegerField()

class FeesStructureSearchForm(forms.Form):
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round','placeholder':'YYYY'}))
    term = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round','placeholder':'1 ,2 ,3'}))
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), widget=forms.Select(attrs={'class':'w3-input w3-border w3-round'}))

class FeesStructureUpdateForm(forms.Form):
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round','placeholder':'YYYY'}))
    term = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round','placeholder':'1, 2, 3'}))
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), widget=forms.Select(attrs={'class':'w3-input w3-border w3-round'}))
    admission = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round'}))
    diary_and_report_book = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round'}))
    interview_fee = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round'}))
    tuition_fee = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round'}))
    computer_lessons = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round'}))
    hot_lunch = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-round'}))

    
