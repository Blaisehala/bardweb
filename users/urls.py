

from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('register/', views.register, name='users-register'), 
    path('login/', views.user_login_view, name='login'), 
    path('logout/', views.user_logout_view, name='logout'),
    path('payment-instructions/', views.payment_instructions, name='payment_instructions'), 

   # Member Platform
    path('dashboard/', views.member_dashboard, name='member_dashboard'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('directory/', views.alumni_directory, name='alumni_directory'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),

]
