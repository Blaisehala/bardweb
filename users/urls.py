

from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('register', views.register, name='users-register'), 
  

]
