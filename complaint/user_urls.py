from django.urls import path
from . import views

urlpatterns = [
    path('complaints', views.user_view_complaints,
         name='user_complaints_view')
]