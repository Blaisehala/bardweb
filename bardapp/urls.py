


from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'), 
    path('members/',views.members, name='bard-members'),
    path('events/',views.events, name='bard-events'),
    path('memberbenefits/',views.memberbenefits, name='memberbenefits'),

]

