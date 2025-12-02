

from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('register/', views.register, name='users-register'), 
    path('login/', views.user_login_view, name='login'), 
    path('logout/', views.user_logout_view, name='logout'),
    path('payment-instructions/', views.payment_instructions, name='payment_instructions'), 

  

]
