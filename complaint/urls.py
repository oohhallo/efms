from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('complaints', views.admin_view_complaints,
         name='admin_complaints_view'),
]