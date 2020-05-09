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
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('admin_complaints_view'))

        else:
            return render(request, 'complaint/login.html', {'fail': True})
    return render(request, 'complaint/login.html')
