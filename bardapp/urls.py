


from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'), 
    path('members/',views.members, name='\members'),
    path('events/',views.events, name='\events'),

]

