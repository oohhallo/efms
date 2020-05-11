from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logged-out', views.logging_out_view, name='logout'),
    path('signup', views.sign_up_view, name='signup')
    
]