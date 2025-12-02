from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm
from django.contrib.auth import authenticate,login  




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        form.request = request  # Pass request to form for rate limiting
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'pleasecorrect the errors below')
                             
    else:
        form = UserRegisterForm()
    return render (request, 'users/register.html', {'form':form})





def user_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('bard-members')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')




def payment_instructions(request):
    """Display payment instructions page"""
    return render (request, 'users/payment_instructions.html')








# username = form.cleaned_data.get('username')