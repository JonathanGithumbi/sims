from audioop import reverse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from user_account.forms import LoginForm
from django.contrib import messages
from administrator.views import admin_dashboard
def login_view(request):
    """This view logs the user in after authenticating using the email fiels as the username"""
    if request.method == 'POST':
        #create a form instance and bound post data to it
        form = LoginForm(request.POST)
        if form.is_valid():#no errors
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is None:# incorrect username and password
                form.add_error('username',"Incorrect Username or Password")
                return render(request, 'user_account/login.html',{'form':form})
            else:#legit user
                login(request, user)
                return HttpResponseRedirect(reverse('administrator_dashboard'))

        else:#Form has errors
            return render(request, 'user_account/login.html',{'form':form})

    if request.method == 'GET':
        form = LoginForm()
        return render(request,'user_account/login.html',{'form': form})

def logout_view(request):
    """This view logs a user out"""
    logout(request)
    return HttpResponseRedirect(reverse('login'))