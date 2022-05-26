from django.db import models
from user_account.models import CustomUser

class Administrator(models.Model):
    def __str__(self):
        return self.user.email
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,primary_key=True)
    