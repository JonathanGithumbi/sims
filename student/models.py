from tokenize import blank_re
from django.db import models

from user_account.models import CustomUser
from grade.models import Grade
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Student(models.Model):

    def __str__(self):
        return self.first_name+' '+self.middle_name+' '+self.last_name

    GENDER_CHOICES = [
        ('male','Male'),
        ('female','Female')
    ]
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(_("Middle Name"), max_length=50)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length = 6, choices= GENDER_CHOICES)
    date_of_birth = models.DateField()
    grade_admitted_to = models.ForeignKey(Grade,on_delete = models.DO_NOTHING)
    current_grade = models.ForeignKey(Grade,related_name='current_grade',on_delete=models.DO_NOTHING)
    primary_contact_name = models.CharField(max_length = 30, default="Name")
    primary_contact_phone_number = PhoneNumberField(blank=True)
    secondary_contact_name = models.CharField(max_length = 30,default="Name")
    secondary_contact_phone_number = PhoneNumberField(blank=True)
    # optionals 
    hot_lunch = models.BooleanField(default=False)
    transport = models.BooleanField(default=False)
    transport_fee = models.IntegerField(default=3000)
    
