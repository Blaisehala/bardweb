

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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

    # Profile
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),

    path('donate/',views. donate, name='donate'),
    path('donation/success/<int:donation_id>/',views. donation_success, name='donation_success'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


