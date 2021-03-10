from django.urls import path
from . import views

urlpatterns = [
    path('all_complaints', views.all_complaints_view, name='all_complaints_view'),
    path('vote', views.add_vote, name='vote'),
    path('remove_vote', views.remove_vote, name='remove_vote'),
    path('login', views.login_view, name='login'),
    path('', views.login_view, name='login'),
    path('logged-out', views.logging_out_view, name='logout'),
    path('signup', views.sign_up_view, name='signup'),
    path('complaint/<int:id>', views.view_complaint_byid, name='view_complaint'),
    path('edit/<int:id>',views.edit_complaint_byid,name='edit_complaint'),
    path('edit/<int:id>',views.edit_complaint_byid,name='edit_dialog'),
    path('delete/<int:cmp_id>', views.delete_complaint_byid, name='delete_complaint')
]

