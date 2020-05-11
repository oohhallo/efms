from django.shortcuts import render
from .models import Complaint
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .decorators import unauthenticated_user, admin_only
from .forms import RegisterComplaintForm


@login_required(login_url='login')
@admin_only
def admin_view_complaints(request):
    complaints = Complaint.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    zero_complaints=complaints.count() == 0
    return render(request, 'complaint/complaints_table.html',
                  context={'complaints': complaints , 'is_admin': True,
                           'zero_complaints':zero_complaints, 'home_header':'active'})

@login_required(login_url='login')
def user_view_complaints(request):
    log_in_user = User.objects.filter(username=request.user.username).first()
    print(log_in_user)
    complaints = Complaint.objects.filter(author=log_in_user).order_by('created_date')
    print(complaints)
    no_of_complaints=len(complaints)
    return render(request, 'complaint/complaints_table.html',
                  context={'complaints': complaints, 'is_user': True, 'user_name':log_in_user, 'no_of_complaints':no_of_complaints,
                 'home_header':'active'})


@login_required
def logging_out_view(request):
    logout(request)
    return render(request, 'complaint/logout.html')
    
@unauthenticated_user
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
    
@login_required(login_url='login')
def register_complaint_page(request):
    if(request.method == 'POST'):
        print(request)
        form = RegisterComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.author = request.user
            complaint.save()
            return render(request, 'complaint/register_complaint.html',
                   context={"form_saved": True,
                             "register_header": 'active'})
        return render(request, 'complaint/register_complaint.html',
                      context={"invalid_form": True,
                               "register_header": 'active'})
    return render(request, 'complaint/register_complaint.html',
                  context={"register_header": 'active'})
