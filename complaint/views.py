from django.shortcuts import render
from .models import Complaint
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def admin_view_complaints(request):
    complaints = Complaint.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'complaint/complaints_table.html',
                  context={'complaints': complaints})

def login_view(request):
    if(request.method == 'POST'):
        username = request.POST.get("username")
        password = request.POST.get("password")
        is_admin = request.POST.get("is_admin")
        user = authenticate(username=username, password=password)
        if user:
            if is_admin=='on':
                if user.profile.is_admin:
                    login(request,user)
                    return HttpResponseRedirect(reverse('admin_complaints_view'))
                return
            login(request,user)
            if user.profile.is_admin:
                return HttpResponseRedirect(reverse('admin_complaints_view'))

    return render(request, 'complaint/login.html')
