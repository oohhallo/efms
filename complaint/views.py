from django.shortcuts import render
from .models import Complaint, Remark, CATEGORY_CHOICES
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decorators import unauthenticated_user, admin_only,allow_user
from .forms import RegisterComplaintForm, UserRegistrationForm
from django.db.models import Q

@login_required(login_url='login')
@admin_only
def admin_view_complaints(request):
    complaints = Complaint.objects.filter(~Q(status = 'closed')).order_by('created_date')
    filter_by = request.GET.get('filter_by_category')
    if(request.user.profile.head_of != 'other'):
        complaints = Complaint.objects.filter(~Q(status = 'closed'), ~Q(status = 'comlpeted'),category=request.user.profile.head_of)
    
    if filter_by in [i[0] for i in CATEGORY_CHOICES]:
        complaints=Complaint.objects.filter(~Q(status = 'closed'), category=filter_by)
    zero_complaints=complaints.count() == 0
    return render(request, 'complaint/complaints_table.html',
                  context={'complaints': complaints , 'is_admin': True,
                           'zero_complaints':zero_complaints, 'home_header':'active',
                           'view_url': reverse('admin_complaints_view')})

@login_required(login_url='login')
def user_view_complaints(request):
    log_in_user = User.objects.filter(username=request.user.username).first()
    complaints = Complaint.objects.filter(author=log_in_user).order_by('created_date')
    filter_by = request.GET.get('filter_by_category')
    if filter_by in [i[0] for i in CATEGORY_CHOICES]:
        complaints=Complaint.objects.filter(category=filter_by,author=log_in_user)
    no_of_complaints=len(complaints)
    return render(request, 'complaint/complaints_table.html',
                  context={'complaints': complaints, 'is_user': True, 
                  'user_name':log_in_user, 'no_of_complaints':no_of_complaints,
                 'home_header':'active', 'view_url': reverse('user_complaints_view')})

@login_required(login_url='login')
def logging_out_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required(login_url='login')
@allow_user
def view_complaint_byid(request, id):
    complaint = Complaint.objects.filter(id=id)[0]
    if request.method == "POST":
        status = request.POST.get('status')
        remark = request.POST.get('remark')
        complaint.status = status
        complaint.save()
        Remark.objects.create(text=remark, complaint=complaint,
                               author=request.user)

    remarks = Remark.objects.filter(complaint=complaint)
    return render(request, 'complaint/view_complaint.html',
                  {'complaint': complaint, "remarks": remarks,
                   'status_choices': Complaint.STATUS_CHOICES})
    
@unauthenticated_user
def login_view(request):
    if(request.method == 'POST'):
        username = request.POST.get("username")
        password = request.POST.get("password")
        is_admin = request.POST.get("is_admin")
        user = authenticate(username=username, password=password)
        if user:
            
            if is_admin =='on' or user.profile.is_admin:
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

@login_required(login_url='login')
def change_password_view(request):
    if(request.method =='POST'):
        old_password = request.POST.get("old_pass")
        new_password1 = request.POST.get("new_pass1")
        new_password2 = request.POST.get("new_pass2")
        if new_password1==new_password2:
            user =authenticate(username= request.user.username, password = old_password)
            if user:
                request.user.set_password(new_password1)
                request.user.save()
                user = authenticate(username= request.user.username, password = new_password1)
                if user:
                    login(request, user)
                    return render(request, 'complaint/change_password.html', context={
                        "pass_changed": True, 'password_header': 'active'
                    })
            else:
                return render(request, 'complaint/change_password.html', context={
                        "old_pass_wrong": True, 'password_header': 'active'
                    })
        else:
            return render(request, 'complaint/change_password.html', context={
                        "pass_mismatch": True, 'password_header': 'active'
                    })

    return render(request, 'complaint/change_password.html',
                  {'password_header': 'active'})


@unauthenticated_user
def sign_up_view(request):
    form=UserRegistrationForm(request.POST)
    if request.method=='POST':
        if form.is_valid():
            print("hello")
            user=form.save()
            login(request,user)
            return HttpResponseRedirect(reverse('user_complaints_view'))
        return HttpResponse("Invalid sign up")

    return render(request, 'complaint/sign_up.html', {'form': form})

@login_required(login_url='login')
def register_complaint_page(request):
    if(request.method == 'POST'):
        form = RegisterComplaintForm(request.POST, request.FILES)
        is_anonymous=request.POST.get("is_anonymous")
        photo = request.POST.get("photo")
        if form.is_valid():
            print(request.POST)
            complaint = form.save(commit=False)
            complaint.author = request.user
            complaint.photo = form.cleaned_data['photo']
            #complaint.photo.save(name=request.POST.get("title")+".png", content="jhkj")
            #complaint.photo.name = str(complaint.id) + ".png"
            if is_anonymous :
                complaint.is_anonymous = True
                complaint.save()
                return render(request, 'complaint/register_complaint.html',
                   context={"form_saved": True,
                             "register_header": 'active'})
            else:
                complaint.save()
                return render(request, 'complaint/register_complaint.html',
                   context={"form_saved": True,
                             "register_header": 'active'})
        return render(request, 'complaint/register_complaint.html',
                      context={"invalid_form": True,
                               "register_header": 'active'})
    return render(request, 'complaint/register_complaint.html',
                  context={"register_header": 'active'})
