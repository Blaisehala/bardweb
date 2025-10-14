


from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # Events
    path('events/', views.events_list, name='events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    
    # News
    path('news/', views.news_list, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    
    # Membership
    path('membership/', views.membership, name='membership'),
    
    # Donations
    path('donate/', views.donate, name='donate'),
    
    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Gallery
    path('gallery/', views.gallery_view, name='gallery'),
    
    # Static Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),]
