from django.shortcuts import render
from .models import Complaint
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


@login_required
def admin_view_complaints(request):
    complaints = Complaint.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'complaint/complaints_table.html',
                  context={'complaints': complaints , 'isit_admin': True})

@login_required
def user_view_complaints(request):
    log_in_user = User.objects.filter(username=request.user.username).first()
    complaints = Complaint.objects.filter(author=log_in_user).order_by('created_date')
    return render(request, 'complaint/complaints_table.html',
                  context={'complaints': complaints, 'isit_user': True, 'user_name':log_in_user})

@login_required
def logging_out_view(request):
    logout(request)
    return render(request, 'complaint/logout.html')
    

def login_view(request):
    if(request.method == 'POST'):
        username = request.POST.get("username")
        password = request.POST.get("password")
        is_admin = request.POST.get("is_admin")
        user = authenticate(username=username, password=password)
        if user:
            
            if is_admin =='on':
                if user.profile.is_admin:
                    login(request,user)
                    return HttpResponseRedirect(reverse('admin_complaints_view'))
                else:
                    return render(request, 'complaint/login.html', {'not_admin': True}) 
            
            else:
                login(request,user)
                return HttpResponseRedirect(reverse('user_complaints_view'))

        else:
            return render(request, 'complaint/login.html', {'login_fail' :True})

    return render(request, 'complaint/login.html')


def sign_up_view(request):
    form=UserCreationForm(request.POST)
    if form.is_valid():
        user=form.save()
        login(request,user)
        return HttpResponseRedirect(reverse('user_complaints_view'))
    return render(request, 'complaint/sign_up.html', {'form': form})