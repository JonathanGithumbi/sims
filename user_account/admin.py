from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from user_account.models import CustomUser
##from administrator.models import Administrator
##
##
##class AdministratorInline(admin.StackedInline):
##    model = Administrator
##    can_delete: False
##    
##
##class UserAdmin(BaseUserAdmin):
##    inlines = (AdministratorInline,)
##
admin.site.register(CustomUser,UserAdmin)